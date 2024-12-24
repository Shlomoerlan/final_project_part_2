import matplotlib.pyplot as plt
from flask import send_file, Blueprint
from io import BytesIO
from app.repository.question_4_repository import calculate_correlation_attack_target
from app.service.question_4_service import create_matrix, calculate_correlation, create_heatmap

question_4_bp = Blueprint('question_4', __name__)

@question_4_bp.route('/correlation')
def show_correlation():
    data = calculate_correlation_attack_target()
    matrix = create_matrix(data)
    correlation = calculate_correlation(matrix)
    fig = create_heatmap(correlation)

    img_buf = BytesIO()
    fig.savefig(img_buf, format='png', bbox_inches='tight')
    img_buf.seek(0)
    plt.close(fig)
    return send_file(img_buf, mimetype='image/png')