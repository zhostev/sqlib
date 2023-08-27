# 导入所需模块
from prefect import task, flow
from prefect.artifacts import create_link_artifact
from prefect.filesystems import LocalFileSystem, S3
from prefect import get_run_logger
import yaml
import pandas as pd
import mlflow
import duckdb
import qlib
from qlib.utils import init_instance_by_config, flatten_dict
from qlib.contrib.eva.alpha import calc_ic
from qlib.contrib.strategy import TopkDropoutStrategy
from qlib.backtest import backtest, executor
from qlib.contrib.report import analysis_model, analysis_position
from qlib.contrib.evaluate import risk_analysis
from qlib.contrib.data.handler import Alpha158
from qlib.data.dataset.handler import DataHandlerLP
from qlib.contrib.report.analysis_position.report import _calculate_report_data
from decorator_switch import second_order_decorator as sod


def load_config():
    with open("workflow_config_lightgbm_Alpha158.yaml", "r") as f:
        config = yaml.safe_load(f)
    return config

CFG = load_config()
USE_PREFECT = CFG["use_prefect"]


@sod(task, enabled=USE_PREFECT, name="model_data_init")
def model_data_init(config):
    provider_uri = config["qlib_init"]["provider_uri"]
    region = config["qlib_init"]["region"]
    use_prefect = config["use_prefect"]
    qlib.init(provider_uri=provider_uri, region=region)
    if use_prefect:
        logger = get_run_logger()
        logger.info("QLib initialized successfully")

    # Initialize model
    model_config = config["task"]["model"]
    model = init_instance_by_config(model_config)
    if use_prefect:
        logger.info(f"Model initialized: {model}")

    # Initialize data
    # data_handler_config = config["task"]["dataset"]["kwargs"]["handler"]
    data_handler_config = config["data_handler_config"]
    hd = Alpha158(**data_handler_config)
    dataset_conf = config["task"]["dataset"]
    dataset_conf["kwargs"]["handler"] = hd
    
    dataset = init_instance_by_config(dataset_conf)
    if use_prefect:
        logger.info(f"Dataset initialized: {dataset}")

    # Reweighter = task_config.get("reweighter", None)
    history = hd.fetch()
    history = history.reset_index()
    history.head()
    execute_sql("history.db", "DROP TABLE IF EXISTS history_db")
    execute_sql("history.db", "CREATE TABLE history_db AS SELECT * FROM history")
    execute_sql("history.db", "SELECT * FROM history_db")

    return model, dataset



@sod(task, enabled=USE_PREFECT, name="train_and_predict")
def train_and_predict(model, dataset):
    model.fit(dataset)
    pred = model.predict(dataset)
    if isinstance(pred, pd.Series):
        pred = pred.to_frame("score")
    pred["date"] = pred.index.get_level_values("datetime")
    params = dict(segments="test", col_set="label", data_key=DataHandlerLP.DK_R)
    label = dataset.prepare(**params)
    execute_sql("pred.db", "DROP TABLE IF EXISTS pred_db")
    execute_sql("pred.db", "CREATE TABLE pred_db AS SELECT * FROM pred")
    execute_sql("pred.db", "SELECT * FROM pred_db")
    return pred, label


def execute_sql(db_name, sql):
    con = duckdb.connect(db_name)
    con.sql(sql)


@sod(task, enabled=USE_PREFECT, name="strategy")
def strategy_simulator(config, pred):
    STRATEGY_CONFIG = config["port_analysis_config"]["strategy"]["kwargs"]
    STRATEGY_CONFIG["signal"] = pred
    strategy_obj = TopkDropoutStrategy(**STRATEGY_CONFIG)

    EXECUTOR_CONFIG = config["port_analysis_config"]["executor"]["kwargs"]
    executor_obj = executor.SimulatorExecutor(**EXECUTOR_CONFIG)

    return strategy_obj, executor_obj


@sod(task, enabled=USE_PREFECT, name="backtest_record")
def backtest_record(config, strategy_obj, executor_obj):
    backtest_config = config["port_analysis_config"]["backtest"]
    portfolio_metric_dict, indicator_dict = backtest(
        executor=executor_obj, strategy=strategy_obj, **backtest_config
    )

    FREQ = backtest_config['freq']
    analysis_freq = "{0}{1}".format(*qlib.utils.time.Freq.parse(FREQ))
    portfolio_metrics = portfolio_metric_dict.get(analysis_freq)
    report_normal = portfolio_metrics[0]
    positions_normal = portfolio_metrics[1]

    # convert report_normal to DataFrame and store it in database
    report_df = report_normal.copy()
    cumreport_df = _calculate_report_data(report_df)
    cumreport_df = cumreport_df.iloc[1:]
    cumreport_df.index = pd.to_datetime(cumreport_df.index)
    cumreport_df["date"] = cumreport_df.index
    execute_sql("report_normal.db", "DROP TABLE IF EXISTS report")
    execute_sql("report_normal.db", "CREATE TABLE report AS SELECT * FROM cumreport_df")
    execute_sql("report_normal.db", "SELECT * FROM report")

    # get indicators_normal
    indicators_normal = indicator_dict.get(analysis_freq)[0]
    indicators_df = indicators_normal.copy()
    # indicators_df = _calculate_report_data(indicators_df)
    indicators_df = indicators_df.iloc[1:]
    indicators_df.index = pd.to_datetime(indicators_df.index)
    indicators_df["date"] = indicators_df.index
    execute_sql("indicators_normal.db", "DROP TABLE IF EXISTS indicators")
    execute_sql(
        "indicators_normal.db", "CREATE TABLE indicators AS SELECT * FROM indicators_df"
    )
    execute_sql("indicators_normal.db", "SELECT * FROM indicators")

    # return results
    return report_df, indicators_normal


@sod(task, enabled=USE_PREFECT, name="risk_analysis")
def risk_analysis_(report_normal):
    analysis = dict()
    analysis["excess_return_without_cost"] = risk_analysis(
        report_normal["return"] - report_normal["bench"]
    )
    analysis["excess_return_with_cost"] = risk_analysis(
        report_normal["return"] - report_normal["bench"] - report_normal["cost"]
    )
    analysis_df = pd.concat(analysis)
    execute_sql("analysis_df.db", "DROP TABLE IF EXISTS analysis")
    execute_sql("analysis_df.db", "CREATE TABLE analysis AS SELECT * FROM analysis_df")
    execute_sql("analysis_df.db", "SELECT * FROM analysis")

    return analysis_df


# 定义流程
@sod(flow, enabled=USE_PREFECT, name="qlib_workflow", description="Demo Prefect")
def run_workflow(config=CFG, name="qlib_workflow"):
    mlflow.set_tracking_uri("http://localhost:5000")
    mlflow.set_experiment("zhanyuan")
    with mlflow.start_run() as run:
        mlflow.lightgbm.autolog()
        
        model, dataset = model_data_init(config)
        pred, label = train_and_predict(model, dataset)
        strategy_obj, executor_obj = strategy_simulator(config, pred)
        backtest_record(config, strategy_obj, executor_obj)
