"""PostgreSQL 연결 — SQLAlchemy engine / session."""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from core.config import settings

engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    """FastAPI Depends용 DB 세션."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
