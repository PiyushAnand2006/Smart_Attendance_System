"""Attendance Models."""
from datetime import date, datetime

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String

from app.db import Base, ModelMixin


class AttendanceSession(Base, ModelMixin):
    __tablename__ = 'attendance_sessions'

    id = Column(Integer, primary_key=True)
    session_id = Column(String(32), unique=True, nullable=False)
    subject_id = Column(Integer, ForeignKey('subjects.id'), nullable=False)
    class_id = Column(Integer, ForeignKey('classes.id'), nullable=False)
    faculty_id = Column(Integer, nullable=True)
    attendance_mode = Column(String(16), nullable=False, default='FACE')
    status = Column(String(16), nullable=False, default='active')
    total_students = Column(Integer, nullable=False, default=0)
    scheduled_date = Column(Date, nullable=True)
    created_at = Column(DateTime, nullable=True, default=datetime.utcnow)


class AttendanceRecord(Base, ModelMixin):
    __tablename__ = 'attendance_records'

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False, index=True)
    session_id = Column(Integer, ForeignKey('attendance_sessions.id'), nullable=False, index=True)
    status = Column(String(16), nullable=False, default='PRESENT')
    attendance_method = Column(String(16), nullable=False, default='FACE')
    attendance_date = Column(Date, nullable=True)
    created_at = Column(DateTime, nullable=True, default=datetime.utcnow)
