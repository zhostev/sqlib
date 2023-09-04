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


# 导入sklearn.metrics中的相关函数
# from sklearn.metrics import accuracy_score, r2_score, recall_score
from sklearn.metrics import mean_squared_error, r2_score


# 定义任务
@task(name="load_config")
def load_config():
    with open("config/workflow_config_lightgbm_Alpha158.yaml", "r") as f:
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
    model_config_1 = config["task"]["model_1"]
    model_1 = init_instance_by_config(model_config_1)
    logger.info(f"Model initialized: {model_1}")
    
    model_config_2 = config["task"]["model_2"]
    model_2 = init_instance_by_config(model_config_2)
    logger.info(f"Model initialized: {model_2}")

    # Initialize data
    data_handler_config = config["data_handler_config"]
    hd = Alpha158(**data_handler_config)
    dataset_conf = config["task"]["dataset"]
    dataset_conf["kwargs"]["handler"] = hd

    dataset = init_instance_by_config(dataset_conf)
    logger.info(f"Dataset initialized: {dataset}")

    history = hd.fetch()
    history = history.reset_index()
    history.head()

    save_to_db("history.db", "history_db", history)

    return (model_1, model_2), dataset


@task(name="train_and_predict")
def train_and_predict(models, dataset):
    # Unpack models
    model_1, model_2 = models

    # Train and predict with model_1
    model_1.fit(dataset)
    pred_1 = model_1.predict(dataset)
    
    # # Train and predict with model_2
    # model_2.fit(dataset)
    # pred_2 = model_2.predict(dataset)
    
    # # Combine predictions
    # pred = pd.concat([pred_1, pred_2], axis=1)
    pred = pred_1.copy()
    
    # Post-processing
    if isinstance(pred, pd.Series):
        pred = pred.to_frame("score")
    pred["date"] = pred.index.get_level_values("datetime")
    params = dict(segments="test", col_set="label", data_key=DataHandlerLP.DK_R)
    label = dataset.prepare(**params)

    save_to_db("pred.db", "pred_db", pred)
    return pred, label



@task(name="strategy")
def strategy_simulator(config, pred):
    STRATEGY_CONFIG = config["port_analysis_config"]["strategy"]["kwargs"]
    STRATEGY_CONFIG["signal"] = pred
    strategy_obj = TopkDropoutStrategy(**STRATEGY_CONFIG)

    EXECUTOR_CONFIG = config["port_analysis_config"]["executor"]["kwargs"]
    executor_obj = executor.SimulatorExecutor(**EXECUTOR_CONFIG)

    return strategy_obj, executor_obj


@task(name="backtest_record")
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

    save_to_db("report_normal.db", "report_db", cumreport_df)

    # get indicators_normal
    indicators_normal = indicator_dict.get(analysis_freq)[0]
    indicators_df = indicators_normal.copy()
    # indicators_df = _calculate_report_data(indicators_df)
    indicators_df = indicators_df.iloc[1:]
    indicators_df.index = pd.to_datetime(indicators_df.index)
    indicators_df["date"] = indicators_df.index

    save_to_db("indicators_normal.db", "indicators_db", indicators_df)

    # return results
    return report_df, indicators_normal


@task(name="risk_analysis")
def riskanalysis(report_normal):
    analysis = dict()
    analysis["excess_return_without_cost"] = risk_analysis(
        report_normal["return"] - report_normal["bench"]
    )
    analysis["excess_return_with_cost"] = risk_analysis(
        report_normal["return"] - report_normal["bench"] - report_normal["cost"]
    )
    analysis_df = pd.concat(analysis)

    save_to_db("analysis_df.db", "analysis_db", analysis_df)

    return analysis_df

@task(name="get_group_return")
def group_return(config, pred_df: pd.DataFrame = None, label_df: pd.DataFrame = None, reverse: bool = False, N: int = 5, **kwargs):
    N = config.get("n_group", N)
    pred_label = pd.concat([label_df, pred_df], axis=1, sort=True)
    pred_label.columns.values[0] = 'label'    
    kwargs['rangebreaks'] = config.get('rangebreaks')
    group_return_df = get_group_return(pred_label, reverse, N, return_df=True, **kwargs)
    
    save_to_db("group_return.db", "group_return", group_return_df)

    return group_return_df

# 定义用于计算均方误差和R^2的函数
def calculate_mse(pred, label):
    return mean_squared_error(label, pred)

def calculate_r2(pred, label):
    return r2_score(label, pred)



@flow(name="qlib_workflow", description="Demo Prefect")
def run_workflow(name="qlib_workflow"):
    mlflow.set_tracking_uri("http://localhost:5000")
    mlflow.set_experiment("model_workflow")
    with mlflow.start_run() as run:
        mlflow.lightgbm.autolog()
        config = load_config()
        models, dataset = model_data_init(config)
        pred, label = train_and_predict(models, dataset)
        
        # 检查是否存在 NaN 值
        if pred.isnull().any().any() or label.isnull().any().any():
            # 处理 NaN 值
            pred = pred.fillna(0)
            label = label.fillna(0)

        # 假设 pred 是一个 pandas DataFrame
        pred = pred.drop(columns='date')

        # 计算额外的指标
        # pred的第一列来计算mse
        
        
        mse_1 = calculate_mse(pred.iloc[:, 0], label.values) 
        r2_1 = calculate_r2(pred.iloc[:, 0], label.values)
        # mse_2 = calculate_mse(pred.iloc[:, 1], label.values)
        # r2_2 = calculate_r2(pred.iloc[:, 1], label.values)

        # 记录额外的指标
        mlflow.log_metric("mse_1", mse_1)
        mlflow.log_metric("r2_1", r2_1)
        # mlflow.log_metric("mse_2", mse_2)
        # mlflow.log_metric("r2_2", r2_2)


        strategy_obj, executor_obj = strategy_simulator(config, pred)
        backtest_record(config, strategy_obj, executor_obj)


        # 计算额外的指标


        strategy_obj, executor_obj = strategy_simulator(config, pred)
        backtest_record(config, strategy_obj, executor_obj)

