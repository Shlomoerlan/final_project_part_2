from datetime import datetime
from typing import List
import plotly.graph_objects as go
from io import BytesIO
from sqlalchemy import func
from toolz import curry
from app.db.models import Event
from app.dto.trend_analysis import TrendAnalysis

def get_month_name(month: int) -> str:
    if not month or month < 1 or month > 12:
        return 'Unknown'
    try:
        return datetime.strptime(str(month), "%m").strftime("%B")
    except ValueError:
        return 'Unknown'




def create_time_series_plot(data: List[TrendAnalysis], title: str) -> BytesIO:
    """יצירת גרף והמרתו ל-BytesIO"""
    fig = go.Figure()

    # סינון נתונים לא תקינים
    valid_data = [d for d in data if d.time_period != 'Unknown']

    # הוספת קו התדירות
    fig.add_trace(
        go.Scatter(
            x=[d.time_period for d in valid_data],
            y=[d.frequency for d in valid_data],
            mode='lines+markers',
            name='Frequency',
            line=dict(color='blue', width=2),
            marker=dict(size=8)
        )
    )

    # הוספת עמודות הספירה
    fig.add_trace(
        go.Bar(
            x=[d.time_period for d in valid_data],
            y=[d.count for d in valid_data],
            name='Count',
            yaxis='y2',
            opacity=0.5
        )
    )

    # עדכון העיצוב
    fig.update_layout(
        title=title,
        xaxis_title="Time Period",
        yaxis_title="Attack Frequency",
        yaxis2=dict(
            title="Attack Count",
            overlaying='y',
            side='right'
        ),
        template='plotly_white',
        showlegend=True,
        hovermode='x'
    )

    # המרה לתמונה
    img_bytes = BytesIO()
    fig.write_image(img_bytes, format='png')
    img_bytes.seek(0)
    return img_bytes

@curry
def get_monthly_trends(session, year: int) -> List[TrendAnalysis]:
    """קבלת מגמות חודשיות עם טיפול בחודשים לא תקינים"""
    monthly_counts = (
        session.query(
            Event.imonth,
            func.count(Event.event_id).label('count')
        )
        .filter(Event.iyear == year)
        .filter(Event.imonth.isnot(None))  # סינון ערכי null
        .group_by(Event.imonth)
        .order_by(Event.imonth)
        .all()
    )

    total_months = 12
    return [
        TrendAnalysis(
            time_period=get_month_name(month),  # שימוש בפונקציית ההמרה החדשה
            count=count,
            frequency=count / total_months
        )
        for month, count in monthly_counts
    ]

