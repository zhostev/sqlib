import os
import qlib
import mlflow
import pandas as pd
from config_handler.config_handler import load_config
from data_handler.data_handler import initialize_data_handler, load_dataset
from model_handler.model_handler import initialize_model, train_model, handle_predictions
from strategy_executor.strategy_executor import initialize_strategy, initialize_executor
from database_utils.db_utils import save_to_db, DuckDBManager
from utils.calc_group_return import get_group_return
from sklearn.metrics import mean_squared_error, r2_score

def calculate_mse(pred, label):
    return mean_squared_error(label, pred)

def calculate_r2(pred, label):
    return r2_score(label, pred)

def get_labels_from_handler(handler):
    # You need to determine the exact function to fetch labels, placeholder here
    return handler.fetch(col_set='label')  # Assuming 'label' is the col_set for labels

def run_workflow():
    config = load_config()
    
    # Initialize QLib
    qlib.init(provider_uri=config['qlib_init']['provider_uri'], region=config['qlib_init']['region'])

    # Ensure the database directory exists
    db_directory = 'database_utils/duckdb_files'
    os.makedirs(db_directory, exist_ok=True)

    # Initialize Data Handling
    data_handler = initialize_data_handler(config['data_handler_config'])
    dataset, history = load_dataset(config, data_handler)
    
    save_to_db(db_directory, 'history.db', 'history_db', history)

    # Initialize Models
    model = initialize_model(config, 'model')
    pred = train_model(model, dataset)
    
    # Debug 输出预测结果的头几行
    print("Prediction DataFrame (after train_model): \n", pred.head())

    handle_predictions = lambda df: df
    pred = handle_predictions(pred)

    # 再次检查并确认预测结果中的列和索引
    # print("Prediction DataFrame columns (after handling):", pred.columns)

    # 确保预测结果包含 'datetime' 和 'instrument' 列
    if 'datetime' not in pred.columns or 'instrument' not in pred.columns:
        raise KeyError("Prediction DataFrame does not contain 'datetime' and 'instrument' columns.")

    save_to_db(db_directory, 'pred.db', 'pred_db', pred)

    # Fetch and handle true labels
    true_labels = get_labels_from_handler(data_handler).reset_index()
    print("True labels DataFrame columns:", true_labels.columns)
    true_labels = true_labels.set_index(['datetime', 'instrument'])

    # 确保预测结果也使用相同的索引
    pred = pred.set_index(['datetime', 'instrument'])
    true_labels = true_labels['LABEL0']
    pred, true_labels = pred.align(true_labels, join='inner')

    # 计算额外的指标
    mse = calculate_mse(pred['score'], true_labels)
    r2 = calculate_r2(pred['score'], true_labels)

    # Initialize and run strategy
    strategy = initialize_strategy(config, pred)
    exec = initialize_executor(config)

    portfolio_metric_dict, indicator_dict = exec.run(strategy)
    report, indicators = portfolio_metric_dict.get('all')[0], indicator_dict.get('day')[0]

    save_to_db(db_directory, 'report_normal.db', 'report_db', report)
    save_to_db(db_directory, 'indicators_normal.db', 'indicators_db', indicators)

    # Log metrics with mlflow
    mlflow.set_tracking_uri('http://localhost:5000')
    mlflow.set_experiment('model_workflow')
    with mlflow.start_run() as run:
        mlflow.log_metric('mse', mse)
        mlflow.log_metric('r2', r2)

        for metric_name, value in report.items():
            if isinstance(value, (int, float)):
                mlflow.log_metric(f'backtest_metric_{metric_name}', value)

if __name__ == '__main__':
    run_workflow()

if __name__ == '__main__':
    run_workflow()