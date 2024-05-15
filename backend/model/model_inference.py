from qlib.workflow import R

def load_model(record_id, experiment_name="tutorial_exp"):
    """
    加载训练好的模型
    :param record_id: 实验记录ID
    :param experiment_name: 实验名称
    :return: 训练好的模型
    """
    rec = R.get_recorder(recorder_id=record_id, experiment_name=experiment_name)
    return rec.load_object("trained_model")

def load_prediction(record_id, experiment_name="tutorial_exp"):
    """
    加载模型预测结果
    :param record_id: 实验记录ID
    :param experiment_name: 实验名称
    :return: 模型预测结果
    """
    rec = R.get_recorder(recorder_id=record_id, experiment_name=experiment_name)
    return rec.load_object("pred.pkl")