from qlib.utils import init_instance_by_config
from qlib.contrib.data.handler import DataHandlerLP
from data_handler.alpha158 import Alpha158

def initialize_data_handler(data_handler_config):
    return Alpha158(**data_handler_config)

def load_dataset(config, handler):
    dataset_conf = config["task"]["dataset"]
    dataset_conf['kwargs']['handler'] = handler
    dataset = init_instance_by_config(dataset_conf)
    # Ensure fetching in the correct format
    fetched_data = handler.fetch()
    return dataset, fetched_data.reset_index()