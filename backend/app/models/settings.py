"""Settings Models."""
from datetime import datetime

from sqlalchemy import Boolean, Column, Float, Integer, String

from app.db import Base, ModelMixin


class AttendanceThreshold(Base, ModelMixin):
    __tablename__ = 'attendance_thresholds'

    id = Column(Integer, primary_key=True)
    threshold_percentage = Column(Float, nullable=False, default=75.0)
    warning_percentage = Column(Float, nullable=False, default=80.0)
    critical_percentage = Column(Float, nullable=False, default=70.0)
    period_type = Column(String(32), nullable=True, default='overall')
    period_value = Column(String(32), nullable=True)
    department = Column(String(64), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(String(32), nullable=True)
    updated_at = Column(String(32), nullable=True)


class AcademicYear(Base, ModelMixin):
    __tablename__ = 'academic_years'

    id = Column(Integer, primary_key=True)
    year = Column(String(16), nullable=True)
    start_date = Column(String(32), nullable=True)
    end_date = Column(String(32), nullable=True)
    is_current = Column(Boolean, nullable=False, default=False)
    term_1_start = Column(String(32), nullable=True)
    term_1_end = Column(String(32), nullable=True)
    term_2_start = Column(String(32), nullable=True)
    term_2_end = Column(String(32), nullable=True)
    created_at = Column(String(32), nullable=True)


class Timetable(Base, ModelMixin):
    __tablename__ = 'timetable'

    id = Column(Integer, primary_key=True)
    class_id = Column(Integer, nullable=True)
    section_id = Column(Integer, nullable=True)
    subject_id = Column(Integer, nullable=True)
    faculty_id = Column(Integer, nullable=True)
    day_of_week = Column(Integer, nullable=False, default=0)
    start_time = Column(String(16), nullable=True)
    end_time = Column(String(16), nullable=True)
    room = Column(String(32), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
