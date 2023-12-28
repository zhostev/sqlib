# app/routes/model_routes.py
from flask import Blueprint, jsonify
from ..services.model_service import start_model_training, get_training_status

bp = Blueprint('model', __name__, url_prefix='/api/model')

@bp.route('/train', methods=['POST'])
def train_model():
    # 启动模型训练
    start_model_training()
    return jsonify({"message": "Model training started"}), 200

@bp.route('/status', methods=['GET'])
def training_status():
    # 获取模型训练状态
    status = get_training_status()
    return jsonify(status), 200
