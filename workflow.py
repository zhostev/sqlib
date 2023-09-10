# 导入所需模块
from prefect import task, flow
from prefect.artifacts import create_link_artifact
from prefect.filesystems import LocalFileSystem, S3
from prefect import get_run_logger
import yaml
import pandas as pd
import mlflow
import qlib
from qlib.utils import init_instance_by_config, flatten_dict
from qlib.contrib.eva.alpha import calc_ic
from qlib.contrib.strategy import TopkDropoutStrategy
from qlib.backtest import backtest, executor
from qlib.contrib.report import analysis_model, analysis_position
from qlib.contrib.evaluate import risk_analysis
from data_handler.alpha158 import Alpha158
from strategy.topk_dropout import TopkDropoutStrategy
from qlib.data.dataset.handler import DataHandlerLP
from qlib.contrib.report.analysis_position.report import _calculate_report_data
from qlib.data.dataset.loader import QlibDataLoader

from database_utils.db_utils import save_to_db, DuckDBManager
from utils.calc_group_return import get_group_return


import pybroker
from pybroker import Strategy, StrategyConfig, YFinance
from DataSource.qlibdata import qlibDataSource

# 导入sklearn.metrics中的相关函数
# from sklearn.metrics import accuracy_score, r2_score, recall_score
from sklearn.metrics import mean_squared_error, r2_score

# 定义全局变量
CONFIG_FILE = "config/workflow_config_lightgbm_Alpha158.yaml"
DB_PATH = "database_utils/duckdb_files"


# 定义任务
@task(name="load_config")
def load_config():
    with open(CONFIG_FILE, "r") as f:
        config = yaml.safe_load(f)
    return config


@task(name="model_data_init")
def model_data_init(config):
    # Initialize QLib
    provider_uri = config["qlib_init"]["provider_uri"]
    region = config["qlib_init"]["region"]
    qlib.init_qlib(provider_uri=provider_uri, region=region)
    logger = get_run_logger()
    logger.info("QLib initialized successfully")

    # Initialize model
    model_config = config["task"]["model"]
    model = init_instance_by_config(model_config)
    logger.info(f"Model initialized: {model}")

    # Initialize data
    data_handler_config = config["data_handler_config"]
    hd = Alpha158(**data_handler_config)
    dataset_conf = config["task"]["dataset"]
    dataset_conf["kwargs"]["handler"] = hd

    dataset = init_instance_by_config(dataset_conf)
    logger.info(f"Dataset initialized: {dataset}")

    history = hd.fetch()
    history = history.reset_index()
    history.head(10)

    save_to_db(DB_PATH, "qlib.db", "history_db", history)

    return model, dataset


@task(name="train_and_predict")
def train_and_predict(model, dataset):
    # Train and predict with model_1
    model.fit(dataset)
    pred = model.predict(dataset)

    pred = pred.copy()

    # Post-processing
    if isinstance(pred, pd.Series):
        pred = pred.to_frame("score")
    pred["date"] = pred.index.get_level_values("datetime")
    params = dict(segments="test", col_set="label", data_key=DataHandlerLP.DK_R)
    label = dataset.prepare(**params)

    save_to_db(DB_PATH, "qlib.db", "pred_db", pred)
    return pred, label


@task(name="strategy")
def strategy_simulator(config,ctx):
    conf = StrategyConfig(initial_cash=500_000,max_long_positions=1)

    def buy_highest_pred(ctx,pred):
        # If there are no long positions across all tickers being traded:
        if not tuple(ctx.long_positions()):
            ctx.buy_shares = ctx.calc_target_shares(1)
            ctx.hold_bars = 2
            ctx.score = ctx.volume[-1]

    strategy = Strategy(qlibDataSource(), "6/1/2021", "12/1/2021",config=conf)
    strategy.add_execution(buy_highest_pred, config=config["market"])
    result = strategy.backtest()
    
    save_to_db(DB_PATH, "qlib.db", "portfolio", result.portfolio)
    save_to_db(DB_PATH, "qlib.db", "positions", result.positions)
    save_to_db(DB_PATH, "qlib.db", "trades", result.trades)
    save_to_db(DB_PATH, "qlib.db", "orders", result.orders)
    save_to_db(DB_PATH, "qlib.db", "metrics_df", result.metrics_df)
    
    return result


@flow(name="workflow")
def workflow():
    mlflow.set_tracking_uri("http://localhost:5000")
    mlflow.set_experiment("model_workflow")
    with mlflow.start_run() as run:
        mlflow.lightgbm.autolog()
        config = load_config()
        model, dataset = model_data_init(config)
        pred, label = train_and_predict(model, dataset)
        strategy_result = strategy_simulator(config, pred)
    