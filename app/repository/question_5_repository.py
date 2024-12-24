from datetime import datetime
from typing import List
from sqlalchemy import extract, func
from toolz import curry
from app.db.models import Event
from app.dto.trend_analysis import TrendAnalysis


@curry
def get_yearly_trends(session) -> List[TrendAnalysis]:
    yearly_counts = (
        session.query(
            extract('year', func.make_date(Event.iyear, 1, 1)).label('year'),
            func.count(Event.event_id).label('count')
        )
        .group_by('year')
        .order_by('year')
        .all()
    )
    total_years = len(yearly_counts)
    return [
        TrendAnalysis(
            time_period=str(year),
            count=count,
            frequency=count / total_years
        )
        for year, count in yearly_counts
    ]


@curry
def get_monthly_trends(session, year: int) -> List[TrendAnalysis]:
    monthly_counts = (
        session.query(
            Event.imonth,
            func.count(Event.event_id).label('count')
        )
        .filter(Event.iyear == year)
        .group_by(Event.imonth)
        .order_by(Event.imonth)
        .all()
    )

    total_months = 12
    return [
        TrendAnalysis(
            time_period=datetime.strptime(str(month), "%m").strftime("%B"),
            count=count,
            frequency=count / total_months
        )
        for month, count in monthly_counts
    ]