from typing import Optional, List, Tuple
from sqlalchemy import func, Numeric, desc
from app.db.database import session_maker
from app.db.models import Region, AttackerStatistic, Location, Event


def get_average_casualties_by_region(top_n: Optional[int] = None) -> List[Tuple[str, float]]:
    with session_maker() as session:
        query = (
            session.query(
                Region.region_name,
                func.avg(
                    func.coalesce(
                        func.nullif(func.cast(AttackerStatistic.n_kill, Numeric), float('nan')), 0
                    ) * 2 +
                    func.coalesce(
                        func.nullif(func.cast(AttackerStatistic.n_wound, Numeric), float('nan')), 0
                    )
                ).label("average_casualties")
            )
            .join(Location, Location.region_id == Region.region_id)
            .join(Event, Event.location_id == Location.location_id)
            .join(AttackerStatistic, AttackerStatistic.event_id == Event.event_id)
            .group_by(Region.region_name)
            .order_by(desc("average_casualties"))
        )

        if top_n:
            query = query.limit(top_n)

        results = query.all()
        return results
