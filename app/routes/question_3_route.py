from flask import jsonify, Blueprint, request
from toolz import pipe
from functools import partial
from app.service.question_3_service import display_top_groups_by_casualties, create_bar_chart

question_3_bp = Blueprint('question_3', __name__)

@question_3_bp.route('/api/groups_casualties', methods=['GET'])
@question_3_bp.route('/api/groups_casualties/top-5', methods=['GET'])
def get_attack_types():
    is_top_5 = 'top-5' in request.path
    attack_data = display_top_groups_by_casualties(top_n=5) if is_top_5 else display_top_groups_by_casualties()

    image_src = pipe(
        attack_data,
        partial(create_bar_chart, title="Attack Types by Severity")
    )

    return jsonify({ 'map': f'<img style="max-width: 40rem;" src="{image_src}"/>' }), 200

