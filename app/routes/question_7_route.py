from flask import request, send_file, jsonify, Blueprint
from app.db.database import session_maker
from app.repository.question_7_repository import query_events_by_time_range
from app.service.question_7_service import create_heatmap

question_7_bp = Blueprint('question_7', __name__)

@question_7_bp.route('/terror_heatmap')
def get_terror_heatmap():
    time_range = request.args.get('time', 'month')
    map_type = request.args.get('type', 'standard')
    try:
        with session_maker() as session:
            events_data = query_events_by_time_range(session, time_range)
            map_path = create_heatmap(events_data, map_type, time_range)
            return send_file(
                map_path,
                mimetype='text/html',
                as_attachment=False
            )
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
