import logging
from qlib.data.dataset.loader import QlibDataLoader

# 配置日志，忽略低于 ERROR 级别的日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def get_data_loader():
    config = {
        "feature": ["$close / Ref($close, 10)"],
        "label": ["$close / Ref($close, 10) - 1"]
    }

    logger.info("加载数据配置: %s", config)
    data_loader = QlibDataLoader(config=config)

    logger.info("检查数据中是否存在 NaN 值...")
    data = data_loader.load()
    if data.isnull().values.any():
        logger.warning("数据中包含 NaN 值。请检查数据预处理步骤。")

    return data_loader