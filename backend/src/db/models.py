from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
from ..constants import DEFAULT_QUOTA_REMAIN


engine = create_engine(
    # "mysql+pymysql://user:pass@127.0.0.1:3306/db0?charset=utf8mb4",
    "sqlite:///db0.db",
    echo=True,
)

Base = declarative_base()


class Problem(Base):  # type: ignore
    __tablename__ = "problems"

    id = Column(Integer, primary_key=True)
    level = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    created_by = Column(String, nullable=False)
    description = Column(String, nullable=False)
    options = Column(String, nullable=False)
    answer_id = Column(Integer, nullable=False)
    solution = Column(String, nullable=False)


class Quota(Base):  # type: ignore
    __tablename__ = "quotas"

    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False, unique=True)
    remain = Column(Integer, nullable=False, default=DEFAULT_QUOTA_REMAIN)
    last_reset_date = Column(DateTime, default=datetime.now)


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine, autoflush=False)


def get_db():
    db = Session()
    try:
        yield db
    # except Exception as e:
    #     db.rollback()
    #     raise e
    finally:
        db.close()
