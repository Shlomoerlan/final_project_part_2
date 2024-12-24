from sqlalchemy import extract, func

from app.db.models import Region, Event, Location


def get_region_attack_data(session):
    return session.query(
        Region.region_name,
        extract('year', func.make_date(Event.iyear, 1, 1)).label('year'),
        func.count(Event.event_id).label('attack_count')
    ).join(Location, Event.location_id == Location.location_id)\
     .join(Region, Location.region_id == Region.region_id)\
     .group_by(Region.region_name, 'year')\
     .order_by(Region.region_name, 'year')


def get_region_centers(session):
    return session.query(
        Region.region_name,
        func.avg(Location.latitude).label('avg_latitude'),
        func.avg(Location.longitude).label('avg_longitude')
    ).join(Location, Region.region_id == Location.region_id)\
     .group_by(Region.region_name)\
     .all()
