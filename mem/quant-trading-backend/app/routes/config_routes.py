# app/routes/config_routes.py
from flask import Blueprint, request, jsonify
from ..services.config_service import get_config, save_config

bp = Blueprint('config', __name__, url_prefix='/api/config')

@bp.route('/', methods=['GET'])
def get_configuration():
    # 获取配置信息
    config = get_config()
    return jsonify(config), 200

@bp.route('/', methods=['POST'])
def update_configuration():
    # 更新配置信息
    config_data = request.get_json()
    save_config(config_data)
    return jsonify({"message": "Configuration updated successfully"}), 200
