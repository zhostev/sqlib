import logging
from qlib.workflow import R
from qlib.workflow.record_temp import PortAnaRecord

# 配置日志，忽略低于 ERROR 级别的日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)



def run_backtest(record_id, backtest_config):
    """
    执行回测并生成结果
    :param record_id: 记录 ID
    :param backtest_config: 回测配置
    """
    logger.info("开始回测，记录ID: %s", record_id)
    with R.start(experiment_name="tutorial_exp", recorder_id=record_id, resume=True):
        rec = R.get_recorder()
        
        logger.info("开始生成回测记录...")
        par = PortAnaRecord(rec, backtest_config, "day")
        par.generate()
    
    logger.info("回测完成。")