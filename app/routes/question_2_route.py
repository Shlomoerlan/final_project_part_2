from flask import Blueprint, request, jsonify
from app.repository.question_2_repository import get_average_casualties_by_region
from app.service.question_2_service import create_map_with_regions

question_2_bp = Blueprint('question_2', __name__)

@question_2_bp.route('/api/average_casualties', methods=['GET'])
@question_2_bp.route('/api/average_casualties/top-5', methods=['GET'])
def get_attack_types():
    try:
        is_top_5 = 'top-5' in request.path
        attack_data = get_average_casualties_by_region(top_n=5) if is_top_5 else get_average_casualties_by_region()
        create_map_with_regions(attack_data)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

