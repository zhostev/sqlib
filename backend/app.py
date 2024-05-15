import os
import logging
from configparser import ConfigParser
from qlib.config import REG_CN
import qlib

from model.model_train import train_model
from model.model_inference import load_model, load_prediction
from evaluation.portfolio_analysis import run_backtest

# 配置日志，忽略低于 ERROR 级别的日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)




def main(config_path="config/settings.ini"):
    try:
        # 获取当前工作目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(current_dir, config_path)

        # 检查配置文件路径
        if not os.path.exists(config_path):
            logger.error(f"配置文件未找到: {config_path}")
            raise FileNotFoundError(f"配置文件未找到: {config_path}")

        # 加载配置
        config = ConfigParser()
        logger.info(f"读取配置文件: {config_path}")
        config.read(config_path)

        # 初始化 Qlib 数据库
        data_path = config["DATA"]["data_path"]  # 从配置中读取数据路径
        logger.info(f"初始化 Qlib 数据库，数据路径: {data_path}")
        qlib.init(provider_uri=data_path, region=REG_CN)
        logger.info("Qlib 数据库初始化完成。")

        # 模型配置
        model_config = {
            "class": "LGBModel",
            "module_path": "qlib.contrib.model.gbdt",
            "kwargs": {**dict(config["MODEL"])}
        }
        logger.info(f"模型配置: {model_config}")

        # 回测配置
        backtest_config = {
            "executor": {
                "class": config["EVALUATION"]["executor_class"],
                "module_path": config["EVALUATION"]["executor_module_path"],
                "kwargs": {
                    "time_per_step": "day",
                    "generate_portfolio_metrics": True,
                },
            },
            "strategy": {
                "class": config["EVALUATION"]["strategy_class"],
                "module_path": config["EVALUATION"]["strategy_module_path"],
                "kwargs": {
                    "signal": "<PRED>",
                    "topk": int(config["EVALUATION"]["topk"]),
                    "n_drop": int(config["EVALUATION"]["n_drop"]),
                },
            },
            "backtest": {
                "start_time": config["EVALUATION"]["start_time"],
                "end_time": config["EVALUATION"]["end_time"],
                "account": int(config["EVALUATION"]["account"]),
                "benchmark": config["DATA"]["benchmark"],
                "exchange_kwargs": {
                    "freq": "day",
                    "limit_threshold": 0.095,
                    "deal_price": "close",
                    "open_cost": 0.0005,
                    "close_cost": 0.0015,
                    "min_cost": 5,
                },
            },
        }
        logger.info(f"回测配置: {backtest_config}")

        # 训练模型
        logger.info("开始训练模型...")
        record_id = train_model(model_config)
        logger.info(f"模型训练完成，记录ID：{record_id}")

        # 回测分析
        logger.info("开始回测分析...")
        run_backtest(record_id, backtest_config)
        logger.info("回测分析完成。")

    except Exception as e:
        logger.exception("程序执行失败:", exc_info=e)

if __name__ == "__main__":
    main()