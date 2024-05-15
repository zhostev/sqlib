import logging
from qlib.data.dataset import DatasetH
from .data_handler import get_data_handler

logger = logging.getLogger(__name__)


def get_dataset():
    dh = get_data_handler()
    segments = {
        "train": ("20180101", "20181231"),
        "valid": ("20190101", "20191231"),
        "test": ("20200101", "20201231") 
    }

    logger.info("创建 DatasetH, 分段: %s", segments)
    dataset = DatasetH(dh, segments=segments)

    logger.info("检查数据集是否包含 'feature' 和 'label' 列...")
    for segment in segments:
        data = dataset.prepare(segment, col_set=["feature", "label"])
        if data.isnull().values.any():
            logger.warning(f"{segment} 数据集中包含 NaN 值。请检查数据处理步骤。")

    return dataset
