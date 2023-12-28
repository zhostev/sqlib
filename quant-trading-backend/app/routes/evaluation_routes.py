# app/routes/evaluation_routes.py
from flask import Blueprint, jsonify
from ..services.evaluation_service import get_evaluation_results

bp = Blueprint('evaluation', __name__, url_prefix='/api/evaluation')

@bp.route('/results', methods=['GET'])
def evaluation_results():
    # 获取评估结果
    results = get_evaluation_results()
    return jsonify(results), 200
