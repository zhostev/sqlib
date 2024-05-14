from qlib.utils import init_instance_by_config
import pandas as pd

def initialize_model(config, model_key='model'):
    # Assuming 'task' always exists in config
    model_config = config["task"][model_key]
    return init_instance_by_config(model_config)

def train_model(model, dataset):
    model.fit(dataset)
    return model.predict(dataset)

def handle_predictions(pred):
    if isinstance(pred, pd.Series):
        pred = pred.to_frame("score")
    pred["date"] = pred.index.get_level_values("datetime")
    return pred