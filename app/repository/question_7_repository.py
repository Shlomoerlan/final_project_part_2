from sqlalchemy import func, cast, Float
from toolz import curry
from app.db.models import Event, Location


@curry
def query_events_by_time_range(session, time_range: str = 'month'):
    max_year = session.query(func.max(Event.iyear)).scalar()

    query = (
        session.query(
            cast(Location.latitude, Float).label('latitude'),
            cast(Location.longitude, Float).label('longitude'),
            Event.iyear
        )
        .join(Event, Event.location_id == Location.location_id)
        .filter(
            Location.latitude.isnot(None),
            Location.longitude.isnot(None)
        )
    )
    if time_range == 'month':
        query = query.filter(
            Event.iyear == max_year,
            Event.imonth == session.query(func.max(Event.imonth))
            .filter(Event.iyear == max_year).scalar()
        )
    elif time_range == '3years':
        query = query.filter(Event.iyear >= max_year - 2)
    elif time_range == '5years':
        query = query.filter(Event.iyear >= max_year - 4)

    return query.all()
