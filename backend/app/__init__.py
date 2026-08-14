# SmartAttend - Intelligent Multi-Modal Attendance & Parent Notification System
# Backend Application Package

from app.app import create_app


class _DB:
    """Compatibility shim: run.py historically called db.create_all().

    The SQLite database is created and seeded inside create_app(); this
    shim simply ensures the schema exists if invoked directly.
    """

    def create_all(self):
        from app.db import init_db
        init_db()


db = _DB()

__all__ = ['create_app', 'db']
