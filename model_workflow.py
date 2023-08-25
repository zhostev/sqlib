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


@task(name="load_config")
def load_config():
    with open("workflow_config_lightgbm_Alpha158.yaml", "r") as f:
        config = yaml.safe_load(f)
    return config


@task(name="init")
def init(config):
    provider_uri = config["qlib_init"]["provider_uri"]
    reg = config["qlib_init"]["region"]
    qlib.init_qlib(provider_uri=provider_uri, region=reg)
    logger = get_run_logger()
    logger.info("init qlib success")


@task(name="model_init")
def model_init(config):
    task = config["task"]["model"]
    model = init_instance_by_config(task)
    return model


@task(name="dataset_init")
def dataset_init(config):
    data_handler_config = config["data_handler_config"]
    dataset = Alpha158(**data_handler_config)

    dataset_conf = config["task"]["dataset"]
    dataset = init_instance_by_config(dataset_conf)

    logger = get_run_logger()
    # 输出dataset的信息
    logger.info(f"dataset: {dataset}")

    return dataset


@task(name="train")
def train(model, dataset):
    model.fit(dataset)
    return model


@task(name="predict")
def predict(model, dataset):
    pred = model.predict(dataset)
    if isinstance(pred, pd.Series):
        pred = pred.to_frame("score")
    params = dict(segments="test", col_set="label", data_key=DataHandlerLP.DK_R)
    label = dataset.prepare(**params)
    # 如果存在analysis_df，先删除，再创建
    con = duckdb.connect('pred.db')
    con.sql("DROP TABLE IF EXISTS pred_db")
    con.sql("CREATE TABLE pred_db AS SELECT * FROM pred")
    con.sql("SELECT * FROM pred_db").show()

    return pred, label


@task(name="signal_record")
def signal_record(pred, label):
    ic, ric = calc_ic(pred.iloc[:, 0], label.iloc[:, 0])
    return ic, ric


@task(name="strategy")
def strategy(config, pred):
    STRATEGY_CONFIG = config["port_analysis_config"]["strategy"]["kwargs"]
    STRATEGY_CONFIG["signal"] = pred
    strategy_obj = TopkDropoutStrategy(**STRATEGY_CONFIG)
    return strategy_obj


@task(name="SimulatorExecutor")
def simulator(config, strategy_obj):
    EXECUTOR_CONFIG = config["port_analysis_config"]["executor"]["kwargs"]

    executor_obj = executor.SimulatorExecutor(**EXECUTOR_CONFIG)
    return executor_obj


@task(name="backtest_record")
def backtest_record(config, strategy_obj, executor_obj):
    
    backtest_config = config["port_analysis_config"]["backtest"]
    portfolio_metric_dict, indicator_dict = backtest(executor=executor_obj, strategy=strategy_obj, **backtest_config)

    FREQ = "day"
    analysis_freq = "{0}{1}".format(*qlib.utils.time.Freq.parse(FREQ))
    report_normal, positions_normal = portfolio_metric_dict.get(analysis_freq)
    # report_normal = report_normal.copy()
    # report_normal = _calculate_report_data(report_normal)
    report_df = report_normal.copy()
    fig_list,report_df = _report_figure(report_df)
    # 将index转为日期格式
    # 把第一行数据删除
    report_df = report_df.iloc[1:]
    report_df.index = pd.to_datetime(report_df.index)
    report_df['date'] = report_df.index

    con = duckdb.connect('report_normal.db')
    con.sql("DROP TABLE IF EXISTS report")
    con.sql("CREATE TABLE report AS SELECT * FROM report_df")
    con.sql("SELECT * FROM report").show()
    return report_normal, fig_list


@task(name="risk_analysis")
def riskanalysis(report_normal):
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


@flow(name="qlib_workflow", description="Demo Prefect")
def run_workflow(name="qlib_workflow"):
    mlflow.set_tracking_uri("http://localhost:5000")
    mlflow.set_experiment("zhanyuan")

    with mlflow.start_run() as run:
        config = load_config()
        mlflow.lightgbm.autolog()
        init(config)
        model = model_init(config)
        dataset = dataset_init(config)
        model = train(model, dataset)
        pred, label = predict(model, dataset)
        # ic, ric = signal_record(pred, label)
        strategy_obj = strategy(config, pred)
        executor_obj = simulator(config, strategy_obj)
        report_normal, fig_list = backtest_record(config, strategy_obj, executor_obj)
        analysis_df = riskanalysis(report_normal)
        
        # 把workflow_config_lightgbm_Alpha158.yaml上传到mlflow
        create_link_artifact("workflow_config_lightgbm_Alpha158.yaml", "workflow_config_lightgbm_Alpha158.yaml")



        
