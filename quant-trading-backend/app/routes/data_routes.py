# app/routes/data_routes.py
from flask import Blueprint, jsonify
from ..services.data_service import initiate_data_process, get_data_history

bp = Blueprint('data', __name__, url_prefix='/api/data')

@bp.route('/initiate', methods=['POST'])
def initiate_data():
    # 启动数据处理流程
    initiate_data_process()
    return jsonify({"message": "Data process initiated"}), 200

@bp.route('/history', methods=['GET'])
def data_history():
    # 获取数据处理历史
    history = get_data_history()
    return jsonify(history), 200
