from qlib.contrib.strategy import TopkDropoutStrategy
from qlib.backtest import executor

def initialize_strategy(config, pred):
    strategy_config = config["port_analysis_config"]["strategy"]["kwargs"]
    strategy_config["signal"] = pred
    return TopkDropoutStrategy(**strategy_config)

def initialize_executor(config):
    executor_config = config["port_analysis_config"]["executor"]["kwargs"]
    return executor.SimulatorExecutor(**executor_config)