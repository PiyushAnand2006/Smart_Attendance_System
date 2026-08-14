"""Database layer for SmartAttend.

Uses SQLAlchemy (core + ORM) with a SQLite database so the backend is fully
functional with zero external services. The schema is created on startup and
seeded with demo data via :func:`seed_db`.
"""
import os
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# ---------------------------------------------------------------------------
# Engine / session factory
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DB_PATH = os.path.join(BASE_DIR, 'smartattend.db')

DATABASE_URL = os.environ.get('DATABASE_URL', f'sqlite:///{DEFAULT_DB_PATH}')

# SQLite needs a single shared connection when the dev server is threaded.
_connect_args = {}
if DATABASE_URL.startswith('sqlite'):
    _connect_args = {'check_same_thread': False}

engine = create_engine(
    DATABASE_URL,
    connect_args=_connect_args,
    pool_pre_ping=True,
    future=True,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False, future=True)

Base = declarative_base()


class ModelMixin:
    """Mixin providing a JSON-friendly ``to_dict()`` over table columns."""

    def to_dict(self, exclude=None):
        exclude = exclude or set()
        return {
            c.name: getattr(self, c.name)
            for c in self.__table__.columns
            if c.name not in exclude
        }


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def init_db():
    """Create all tables (idempotent)."""
    # Importing the models package registers every table on ``Base.metadata``.
    from app import models  # noqa: F401
    Base.metadata.create_all(engine)


def reset_db():
    """Drop and recreate all tables (used by tests / fresh start)."""
    from app import models  # noqa: F401
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
