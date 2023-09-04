# 导入所需模块
from prefect import task, flow
from prefect import get_run_logger
import yaml
import pandas as pd
import mlflow
import qlib
from qlib.utils import init_instance_by_config
from qlib.contrib.strategy import TopkDropoutStrategy
from qlib.backtest import backtest, executor
from qlib.contrib.evaluate import risk_analysis
from data_handler.alpha158 import Alpha158
from strategy.topk_dropout import TopkDropoutStrategy
from qlib.data.dataset.handler import DataHandlerLP
from qlib.contrib.report.analysis_position.report import _calculate_report_data

from database_utils.db_utils import save_to_db
from utils.switchable_decorator import second_order_decorator as sod
from datetime import datetime
from utils.calc_group_return import get_group_return
import sys


def load_config():
    config_name = "config/workflow_config_lightgbm_Alpha158_prefect_switchable.yaml"
    with open(config_name, "r") as f:
        config = yaml.safe_load(f)
    return config


IS_DEBUGGING = sys.gettrace()
CFG = load_config() 
USE_PREFECT = True if IS_DEBUGGING else CFG["use_prefect"]
EXP_NAME = CFG['handler_name'] + '_' + str(datetime.now()).split('.')[0].replace(':', '').replace('-', '').replace(' ', '_') 


@sod(task, enabled=USE_PREFECT, name="model_data_init")
def model_data_init(config):
    # Initialize QLib
    use_prefect = config["use_prefect"]    
    provider_uri = config["qlib_init"]["provider_uri"]
    region = config["qlib_init"]["region"]
    qlib.init_qlib(provider_uri=provider_uri, region=region)
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
    # data_loader = QlibDataLoader(config=config['data_loader']['kwargs']['config'])
    # df = data_loader.load(instruments='csi300', start_time='2010-01-01', end_time='2017-12-31')
    
    data_handler_config = config["data_handler_config"]

    handler_class = Alpha158 # if config['handler_name'] == 'Alpha158' else AlphaCustom
    hd = handler_class(**data_handler_config)
    dataset_conf = config["task"]["dataset"]
    dataset_conf["kwargs"]["handler"] = hd

    dataset = init_instance_by_config(dataset_conf)
    if use_prefect:    
        logger.info(f"Dataset initialized: {dataset}")

    # Reweighter = task_config.get("reweighter", None)
    history = hd.fetch()
    history = history.reset_index()
    history.head()

    save_to_db("history.db", "history_" + EXP_NAME, history)

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

    save_to_db("pred.db", "pred_" + EXP_NAME, pred)
    return pred, label


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

    FREQ = "day"
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

    save_to_db("report_normal.db", "report_normal_" + EXP_NAME, cumreport_df)

    # get indicators_normal
    indicators_normal = indicator_dict.get(analysis_freq)[0]
    indicators_df = indicators_normal.copy()
    # indicators_df = _calculate_report_data(indicators_df)
    indicators_df = indicators_df.iloc[1:]
    indicators_df.index = pd.to_datetime(indicators_df.index)
    indicators_df["date"] = indicators_df.index

    save_to_db("indicators_normal.db", "indicators_" + EXP_NAME, indicators_df)

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

    save_to_db("analysis_df.db", "analysis_" + EXP_NAME, analysis_df)

    return analysis_df


@sod(task, enabled=USE_PREFECT, name="group_return")
def group_return(config, pred_df: pd.DataFrame = None, label_df: pd.DataFrame = None, reverse: bool = False, N: int = 5, **kwargs):
    N = config.get("n_group", N)
    pred_label = pd.concat([label_df, pred_df], axis=1, sort=True)
    pred_label.columns.values[0] = 'label'    
    kwargs['rangebreaks'] = config.get('rangebreaks')
    group_return_df = get_group_return(pred_label, reverse, N, return_df=True, **kwargs)
    
    save_to_db("group_return.db", "group_return_" + EXP_NAME, group_return_df)

    return group_return_df


# 定义流程
@sod(flow, enabled=USE_PREFECT, name="qlib_workflow", description="Demo Prefect")
def run_workflow(config=CFG, name="qlib_workflow"):
    mlflow.set_tracking_uri("http://localhost:5000")
    mlflow.set_experiment("Cyberquant")
    with mlflow.start_run() as run:
        mlflow.lightgbm.autolog()
        model, dataset = model_data_init(config)
        pred, label = train_and_predict(model, dataset)
        strategy_obj, executor_obj = strategy_simulator(config, pred)
        report_df, indicators_normal = backtest_record(config, strategy_obj, executor_obj)
        analysis_df = risk_analysis_(report_df)
        group_return_df = group_return(config, pred, label)


if __name__ == "__main__":
    run_workflow()
