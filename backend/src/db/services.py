from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from .models import Quota, Problem
from ..constants import DEFAULT_QUOTA_REMAIN


def get_quota(db: Session, user_id: str) -> Optional[Quota]:
    return db.query(Quota).filter(Quota.user_id == user_id).first()


def create_quota(
    db: Session, user_id: str, remain: int = DEFAULT_QUOTA_REMAIN
) -> Quota:
    quota = Quota(user_id=user_id, remain=remain)
    db.add(quota)
    db.commit()
    db.refresh(quota)
    return quota


def reset_quota(db: Session, user_id: str, remain: int = DEFAULT_QUOTA_REMAIN) -> Quota:
    quota = get_quota(db, user_id)
    if quota is None:
        return create_quota(db, user_id, remain)
    now = datetime.now()
    if now - quota.last_reset_date >= timedelta(hours=24):  # type: ignore
        quota.remain = remain  # type: ignore
        quota.last_reset_date = now  # type: ignore
        db.commit()
        db.refresh(quota)
    return quota


def create_problem(
    db: Session,
    level: str,
    created_by: str,
    description: str,
    answer_id: int,
    solution: str,
    options: str,
) -> Problem:
    problem = Problem(
        level=level,
        created_by=created_by,
        description=description,
        answer_id=answer_id,
        solution=solution,
        options=options,
    )
    db.add(problem)
    db.commit()
    db.refresh(problem)
    return problem


def get_history(db: Session, user_id: str) -> list[Problem]:
    return db.query(Problem).filter(Problem.created_by == user_id).all()
