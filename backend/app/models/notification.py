"""Notification Queue and Log Models."""
from datetime import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text

from app.db import Base, ModelMixin


class NotificationTemplate(Base, ModelMixin):
    __tablename__ = 'notification_templates'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    display_name = Column(String(120), nullable=True)
    content = Column(Text, nullable=True)
    variables = Column(String(255), nullable=True, default='')
    is_active = Column(Boolean, nullable=False, default=True)


class NotificationQueue(Base, ModelMixin):
    __tablename__ = 'notification_queue'

    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('attendance_sessions.id'), nullable=True)
    recipient_number = Column(String(32), nullable=True)
    message = Column(Text, nullable=True)
    status = Column(String(16), nullable=False, default='PENDING')
    created_at = Column(String(32), nullable=True)


class NotificationLog(Base, ModelMixin):
    __tablename__ = 'notification_logs'

    id = Column(Integer, primary_key=True)
    queue_id = Column(Integer, ForeignKey('notification_queue.id'), nullable=True)
    recipient_number = Column(String(32), nullable=True)
    status = Column(String(16), nullable=False, default='PENDING')
    error = Column(Text, nullable=True)
    sent_at = Column(String(32), nullable=True)
