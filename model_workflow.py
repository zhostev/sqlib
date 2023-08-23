import yaml
from prefect import Task
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
from prefect import task, Flow, get_run_logger
from prefect import variables
from prefect.filesystems import LocalFileSystem, S3
from prefect.artifacts import create_link_artifact



class ModelWorkflow(Task):
    def __init__(self, config_file):
        with open(config_file, 'r') as f:
            self.config = yaml.safe_load(f)
        super().__init__()

    def init(self):
        provider_uri = self.config['provider_uri']
        region = self.config['region']
        qlib.init(provider_uri=provider_uri, region=region)
        logger = get_run_logger()
        logger.info("init 初始化成功")

    def model_init(self):
        task = self.config['model']
        model = init_instance_by_config(task)
        return model

    def dataset_init(self):
        data_handler_config = self.config['data_handler_config']
        dataset = Alpha158(**data_handler_config)
        dataset_conf = self.config['dataset_conf']
        dataset_conf['kwargs']['handler'] = dataset
        dataset = init_instance_by_config(dataset_conf)
        return dataset

    def train(self, model, dataset):
        model.fit(dataset)
        return model

    def predict(self, model, dataset):
        pred = model.predict(dataset)
        if isinstance(pred, pd.Series):
            pred = pred.to_frame("score")
        params = dict(segments="test", col_set="label", data_key=DataHandlerLP.DK_R)
        label = dataset.prepare(**params)
        return pred, label

    def signal_record(self, pred, label):
        ic, ric = calc_ic(pred.iloc[:, 0], label.iloc[:, 0])
        for i, (date, value) in enumerate(ic.items()):
            mlflow.log_metric("ic", value, step=i)
        for i, (date, value) in enumerate(ric.items()):
            mlflow.log_metric("rank_ic", value, step=i)
        return ic, ric

    def backtest_record(self, pred, label):
        FREQ = "day"
        STRATEGY_CONFIG = self.config['strategy_config']
        STRATEGY_CONFIG['signal'] = pred
        EXECUTOR_CONFIG = self.config['executor_config']
        backtest_config = self.config['backtest_config']
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
    
    
# 定义main函数，用于执行任务：
def main():
    with Flow("sqlib") as flow:
    workflow = ModelWorkflow('config.yaml')
    workflow.init()
    model = workflow.model_init()
    dataset = workflow.dataset_init()
    model = workflow.train(model, dataset)
    pred, label = workflow.predict(model, dataset)
    ic, ric = workflow.signal_record(pred, label)
    report_df, fig_list = workflow.backtest_record(pred, label)


if __name__ == "__main__":
    main()