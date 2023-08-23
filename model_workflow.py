import yaml
from prefect import task, Flow
from qlib import init
import qlib
from qlib.utils import init_instance_by_config
from qlib.workflow import R
from qlib.workflow.record_temp import SignalRecord, PortAnaRecord
import pandas as pd
import mlflow
from mlflow.entities import Metric
from mlflow.tracking import MlflowClient
from qlib.data.dataset.handler import DataHandlerLP
from qlib.contrib.eva.alpha import calc_ic, calc_long_short_return, calc_long_short_prec
from qlib.contrib.strategy import TopkDropoutStrategy
from qlib.backtest import backtest, executor
from qlib.utils.time import Freq
from qlib.contrib.report import analysis_model, analysis_position
from qlib.contrib.report.analysis_position.report import (
    _report_figure,
    _calculate_report_data,
)
from qlib.contrib.report.analysis_position.score_ic import score_ic_graph, _get_score_ic
import plotly.io as pio
import os
import tempfile
from qlib.contrib.evaluate import risk_analysis
from qlib.contrib.data.handler import Alpha158
from prefect import get_run_logger
from prefect.artifacts import create_link_artifact


@task
def load_config():
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
    mlflow.set_tracking_uri("http://localhost:5000")
    mlflow.set_experiment("zhanyuan")
    return config


@task
def init_qlib(config):
    provider_uri = config["provider_uri"]
    reg = config["region"]
    qlib.init(provider_uri=provider_uri, region=reg)
    logger = get_run_logger()
    logger.info("init 初始化成功")


@task
def model_init(config):
    task = config["model"]
    model = init_instance_by_config(task)
    return model

@task
def dataset_init(config):
    data_handler_config = config["data_handler_config"]
    dataset = Alpha158(**data_handler_config)
    dataset_conf = config["dataset_conf"]
    dataset_conf["kwargs"]["handler"] = dataset
    dataset = init_instance_by_config(dataset_conf)
    return dataset

@task
def train(model, dataset):
    model.fit(dataset)
    return model

@task
def predict(model, dataset):
    pred = model.predict(dataset)
    if isinstance(pred, pd.Series):
        pred = pred.to_frame("score")
    params = dict(segments="test", col_set="label", data_key=DataHandlerLP.DK_R)
    label = dataset.prepare(**params)
    return pred, label

@task
def signal_record(pred, label):
    ic, ric = calc_ic(pred.iloc[:, 0], label.iloc[:, 0])
    for i, (date, value) in enumerate(ic.items()):
        mlflow.log_metric("ic", value, step=i)
    for i, (date, value) in enumerate(ric.items()):
        mlflow.log_metric("rank_ic", value, step=i)
    return ic, ric

@task
def backtest_record(config, pred):
    FREQ = "day"
    STRATEGY_CONFIG = config["strategy_config"]
    STRATEGY_CONFIG["signal"] = pred
    EXECUTOR_CONFIG = config["executor_config"]
    backtest_config = config["backtest_config"]
    strategy_obj = TopkDropoutStrategy(**STRATEGY_CONFIG)
    executor_obj = executor.SimulatorExecutor(**EXECUTOR_CONFIG)
    portfolio_metric_dict, indicator_dict = backtest(
        executor=executor_obj, strategy=strategy_obj, **backtest_config
    )
    analysis_freq = "{0}{1}".format(*Freq.parse(FREQ))
    report_normal, positions_normal = portfolio_metric_dict.get(analysis_freq)
    report_df = report_normal.copy()
    fig_list = _report_figure(report_df)
    return report_df, fig_list

@Flow
def run_workflow(name="sqlib_workflow"):
    with mlflow.start_run() as run:
        config = load_config()
        mlflow.lightgbm.autolog()
        init_qlib(config)
        model = model_init(config)
        dataset = dataset_init(config)
        model = train(model, dataset)
        pred, label = predict(model, dataset)
        ic, ric = signal_record(pred, label)
        report_df, fig_list = backtest_record(config, pred)




def main():
    run_workflow()
    
if __name__ == "__main__":
    main()