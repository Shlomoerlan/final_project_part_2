from typing import Optional, Tuple, List, Any
from requests import Session
from sqlalchemy import func, Numeric, desc, Row
from toolz import compose, curry
from app.db.database import session_maker
from app.db.models import Group, AttackerStatistic, Event


@curry
def create_query_for_top_groups(session: Session, top_n: Optional[int] = None) -> list[Row[tuple[Any, Any]]]:
    calculate_casualties = compose(
        lambda column: func.sum(
            func.coalesce(
                func.nullif(
                    func.cast(column, Numeric),
                    float('nan')
                ),
                0
            )
        )
    )

    query = (
        session.query(
            Group.group_name,
            (
                    calculate_casualties(AttackerStatistic.n_kill * 2) +
                    calculate_casualties(AttackerStatistic.n_wound)
            ).label("total_casualties")
        )
        .join(Event, Event.group_id == Group.group_id)
        .join(AttackerStatistic, AttackerStatistic.event_id == Event.event_id)
        .filter(Group.group_name != "Unknown")
        .group_by(Group.group_name)
        .order_by(desc("total_casualties"))
    )

    return query.limit(top_n).all() if top_n else query.all()


def get_top_groups_by_casualties(top_n: Optional[int] = None) -> List[Tuple[str, float]]:
    with session_maker() as session:
        return create_query_for_top_groups(session, top_n)
