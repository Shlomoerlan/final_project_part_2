from sqlalchemy import func
from app.db.database import session_maker
from app.db.models import AttackType, TargetType, Event


def calculate_correlation_attack_target():
    with session_maker() as session:
        query = (
            session.query(
                AttackType.attacktype_name,
                TargetType.targettype_name,
                func.count(Event.event_id).label("event_count")
            )
            .join(Event, Event.attacktype_id == AttackType.attacktype_id)
            .join(TargetType, Event.targettype_id == TargetType.targettype_id)
            .group_by(AttackType.attacktype_name, TargetType.targettype_name)
            .having(func.count(Event.event_id) > 0)
        )

        results = query.all()
        return results
