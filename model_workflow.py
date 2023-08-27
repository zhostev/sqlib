from pprint import pprint

import yaml
import pandas as pd
import mlflow
from mlflow.entities import Metric
from mlflow.tracking import MlflowClient
import plotly.io as pio
import os
import tempfile
from prefect import task, flow
from prefect.artifacts import create_link_artifact
# from qlib import init
import qlib
from qlib.utils import init_instance_by_config
from qlib.workflow import R
from qlib.workflow.record_temp import SignalRecord, PortAnaRecord
from qlib.data.dataset.handler import DataHandlerLP
from qlib.contrib.eva.alpha import calc_ic
from qlib.contrib.strategy import TopkDropoutStrategy
from qlib.backtest import backtest, executor
from qlib.contrib.report import analysis_model, analysis_position
from qlib.contrib.evaluate import risk_analysis
from qlib.utils import flatten_dict
from qlib.contrib.report.analysis_position.report import (
    _report_figure,
    _calculate_report_data,
)
from qlib.contrib.report.analysis_position.score_ic import score_ic_graph
from qlib.contrib.evaluate import risk_analysis
from qlib.contrib.data.handler import Alpha158


from prefect import get_run_logger
from prefect.artifacts import create_table_artifact
from prefect.filesystems import LocalFileSystem, S3

import duckdb
from decorator_switch import second_order_decorator as sod



def load_config():
    with open("workflow_config_lightgbm_Alpha158.yaml", "r") as f:
        config = yaml.safe_load(f)
    return config

cfg = load_config()
USE_PREFECT = cfg["use_prefect"]


@sod(task, enabled=USE_PREFECT, name="init")
def init(config):
    provider_uri = config["qlib_init"]["provider_uri"]
    reg = config["qlib_init"]["region"]
    qlib.init(provider_uri=provider_uri, region=reg)
    if USE_PREFECT:
        logger = get_run_logger()
        logger.info("init qlib success")


@sod(task, enabled=USE_PREFECT, name="model_init")
def model_init(config):
    task = config["task"]["model"]
    model = init_instance_by_config(task)
    return model


@sod(task, enabled=USE_PREFECT, name="dataset_init")
def dataset_init(config):
    data_handler_config = config["data_handler_config"]
    dataset = Alpha158(**data_handler_config)

    dataset_conf = config["task"]["dataset"]
    dataset = init_instance_by_config(dataset_conf)
    if USE_PREFECT:
        logger = get_run_logger()
        # 输出dataset的信息
        logger.info(f"dataset: {dataset}")

    return dataset


@sod(task, enabled=USE_PREFECT, name="train")
def train(model, dataset):
    model.fit(dataset)
    return model


@sod(task, enabled=USE_PREFECT, name="predict")
def predict(model, dataset):
    pred = model.predict(dataset)
    if isinstance(pred, pd.Series):
        pred = pred.to_frame("score")
    pred['date'] = pred.index.get_level_values("datetime")
    params = dict(segments="test", col_set="label", data_key=DataHandlerLP.DK_R)
    label = dataset.prepare(**params)
    # 如果存在analysis_df，先删除，再创建
    con = duckdb.connect('pred.db')
    con.sql("DROP TABLE IF EXISTS pred_db")
    con.sql("CREATE TABLE pred_db AS SELECT * FROM pred")
    con.sql("SELECT * FROM pred_db").show()

    return pred, label


@sod(task, enabled=USE_PREFECT, name="signal_record")
def signal_record(pred, label):
    ic, ric = calc_ic(pred.iloc[:, 0], label.iloc[:, 0])
    return ic, ric


@sod(task, enabled=USE_PREFECT, name="strategy")
def strategy(config, pred):
    STRATEGY_CONFIG = config["port_analysis_config"]["strategy"]["kwargs"]
    STRATEGY_CONFIG["signal"] = pred
    strategy_obj = TopkDropoutStrategy(**STRATEGY_CONFIG)
    return strategy_obj


@sod(task, enabled=USE_PREFECT, name="SimulatorExecutor")
def simulator(config, strategy_obj):
    EXECUTOR_CONFIG = config["port_analysis_config"]["executor"]["kwargs"]

    executor_obj = executor.SimulatorExecutor(**EXECUTOR_CONFIG)
    return executor_obj


@sod(task, enabled=USE_PREFECT, name="backtest_record")
def backtest_record(config, strategy_obj, executor_obj):
    
    backtest_config = config["port_analysis_config"]["backtest"]
    portfolio_metric_dict, indicator_dict = backtest(executor=executor_obj, strategy=strategy_obj, **backtest_config)

    FREQ = backtest_config['freq']
    analysis_freq = "{0}{1}".format(*qlib.utils.time.Freq.parse(FREQ))
    report_normal, positions_normal = portfolio_metric_dict.get(analysis_freq)

    report_df = report_normal.copy()
    report_df = _calculate_report_data(report_df)
    report_df = report_df.iloc[1:]
    report_df.index = pd.to_datetime(report_df.index)
    report_df['date'] = report_df.index

    con = duckdb.connect('report_normal.db')
    con.sql("DROP TABLE IF EXISTS report")
    con.sql("CREATE TABLE report AS SELECT * FROM report_df")
    con.sql("SELECT * FROM report").show()
    
    # indicators_normal = indicator_dict.get(analysis_freq)[0]
    # indicators_df = indicators_normal.copy()
    # # positions_df有dict转为df
    # indicators_df = pd.DataFrame(indicators_df, index=[0])

    # indicators_df = indicators_df.iloc[1:]
    # indicators_df.index = pd.to_datetime(indicators_df.index)
    # indicators_df['date'] = indicators_df.index
    
    # con = duckdb.connect('indicators_normal.db')
    # con.sql("DROP TABLE IF EXISTS indicators")
    # con.sql("CREATE TABLE indicators AS SELECT * FROM indicators_df")
    # con.sql("SELECT * FROM indicators").show()
    return report_normal


@sod(task, enabled=USE_PREFECT, name="risk_analysis")
def risk_analysis_(report_normal):
    analysis = dict()
    # default frequency will be daily (i.e. "day")
    analysis["excess_return_without_cost"] = risk_analysis(report_normal["return"] - report_normal["bench"])
    analysis["excess_return_with_cost"] = risk_analysis(report_normal["return"] - report_normal["bench"] - report_normal["cost"])

    analysis_df = pd.concat(analysis)  # type: pd.DataFrame
    con = duckdb.connect('analysis_df.db')
    con.sql("DROP TABLE IF EXISTS analysis")
    con.sql("CREATE TABLE analysis AS SELECT * FROM analysis_df")
    con.sql("SELECT * FROM analysis").show()
    # log metrics
    analysis_dict = flatten_dict(analysis_df["risk"].unstack().T.to_dict())
    pprint(analysis_df)
    return analysis_df


@sod(flow, enabled=USE_PREFECT, name="qlib_workflow", description="Demo Prefect")
def run_workflow(config=cfg, name="qlib_workflow"):
    mlflow.set_tracking_uri("http://localhost:5000")
    mlflow.set_experiment("Cyberquant")

    with mlflow.start_run() as run:

        mlflow.lightgbm.autolog()
        init(config)
        model = model_init(config)
        dataset = dataset_init(config)
        model = train(model, dataset)
        pred, label = predict(model, dataset)
        ic, ric = signal_record(pred, label)
        strategy_obj = strategy(config, pred)
        executor_obj = simulator(config, strategy_obj)
        report_normal = backtest_record(config, strategy_obj, executor_obj)
        analysis_df = risk_analysis_(report_normal)
        
        # 把workflow_config_lightgbm_Alpha158.yaml上传到mlflow
        create_link_artifact("workflow_config_lightgbm_Alpha158.yaml", "workflow_config_lightgbm_Alpha158.yaml")