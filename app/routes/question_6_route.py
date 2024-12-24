from flask import Blueprint, request, send_file, jsonify, Flask
from app.db.database import session_maker
from app.service.question_6_service import create_region_attack_change_map

question_6_bp = Blueprint('question_6', __name__)

@question_6_bp.route('/region_changes_map', methods=['GET'])
def get_region_changes_map():
    display_type = request.args.get('type', 'all')
    try:
        with session_maker() as session:
            create_region_attack_change_map(session, display_type)
        map_path = r'C:\Users\1\PycharmProjects\final_project_analyze_part_2\app\templates\terror_attack_changes_map.html'
        return send_file(map_path, mimetype='text/html')
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

