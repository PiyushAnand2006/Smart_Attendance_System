# SmartAttend - Intelligent Multi-Modal Attendance & Parent Notification System
# Backend Application Package

from app.app import create_app


class _DB:
    """Compatibility shim: run.py calls db.create_all().

    The in-memory store is auto-seeded on import, so no schema setup is
    required.
    """

    def create_all(self):
        pass


db = _DB()

__all__ = ['create_app', 'db']
