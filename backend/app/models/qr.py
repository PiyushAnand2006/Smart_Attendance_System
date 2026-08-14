"""QR Code Models."""
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from app.db import Base, ModelMixin


class QRIdentity(Base, ModelMixin):
    __tablename__ = 'qr_identities'

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False, unique=True)
    qr_identifier = Column(String(64), unique=True, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)


class QRToken(Base, ModelMixin):
    """Ephemeral token generated for a live QR attendance session.

    Kept in the database for durability across restarts but expired by
    ``expires_at``.
    """

    __tablename__ = 'qr_tokens'

    id = Column(Integer, primary_key=True)
    token = Column(String(64), unique=True, nullable=False)
    session_id = Column(Integer, ForeignKey('attendance_sessions.id'), nullable=False)
    expires_at = Column(String(32), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
