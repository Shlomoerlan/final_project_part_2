from typing import Optional, Any
from requests import Session
from sqlalchemy import Row, func, desc, Numeric
from toolz import curry, compose
from app.db.models import AttackType, AttackerStatistic, Event


@curry
def create_query_for_attack_types(
        session: Session,
        limit: Optional[int] = None
) -> list[Row[tuple[Any, Any]]]:
    severity_calculation = compose(
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
            AttackType.attacktype_name,
            (
                    severity_calculation(AttackerStatistic.n_kill * 2) +
                    severity_calculation(AttackerStatistic.n_wound)
            ).label("severity_score")
        )
        .join(Event, Event.attacktype_id == AttackType.attacktype_id, isouter=True)
        .join(AttackerStatistic, AttackerStatistic.event_id == Event.event_id, isouter=True)
        .group_by(AttackType.attacktype_name)
        .order_by(desc("severity_score"))
    )

    return query.limit(limit).all() if limit else query.all()
