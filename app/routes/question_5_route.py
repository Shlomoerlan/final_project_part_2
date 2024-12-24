from flask import send_file, Blueprint
from app.db.database import session_maker
from app.repository.question_5_repository import get_yearly_trends
from app.service.question_5_service import get_monthly_trends, create_time_series_plot

question_5_bp = Blueprint('question_5', __name__)

@question_5_bp.route('/monthly/<int:year>')
def monthly_trends(year: int):
    with session_maker() as session:
        try:
            trends = get_monthly_trends(session, year)
            valid_trends = [t for t in trends if t.time_period != 'Unknown']
            if not valid_trends:
                return "No valid data found for this year", 404

            img_bytes = create_time_series_plot(
                valid_trends,
                f"Monthly Terror Attack Trends for {year}"
            )
            return send_file(
                img_bytes,
                mimetype='image/png'
            )
        except Exception as e:
            return str(e), 500


@question_5_bp.route('/yearly')
def yearly_trends():
    with session_maker() as session:
        try:
            trends = get_yearly_trends(session)
            img_bytes = create_time_series_plot(
                trends,
                "Yearly Terror Attack Trends"
            )
            return send_file(
                img_bytes,
                mimetype='image/png'
            )
        except Exception as e:
            return str(e), 500


