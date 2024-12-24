from flask import Flask, jsonify, Blueprint, request
from toolz import pipe
from functools import partial
from app.service.question_1_service import display_attack_types_severity, create_bar_image_src, merge_dicts

question_1_bp = Blueprint('question_1', __name__)


@question_1_bp.route('/api/attack-types', methods=['GET'])
@question_1_bp.route('/api/attack-types/top-5', methods=['GET'])
def get_attack_types():
    is_top_5 = 'top-5' in request.path
    attack_data = display_attack_types_severity(top_n=5) if is_top_5 else display_attack_types_severity()

    image_src = pipe(
        attack_data,
        merge_dicts,
        partial(create_bar_image_src, title="Attack Types by Severity")
    )

    return jsonify({ 'map': f'<img style="max-width: 40rem;" src="{image_src}"/>' }), 200

