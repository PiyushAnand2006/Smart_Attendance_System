"""Subject Models."""
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from app.db import Base, ModelMixin


class Subject(Base, ModelMixin):
    __tablename__ = 'subjects'

    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    code = Column(String(32), unique=True, nullable=False)
    department = Column(String(64), nullable=True)
    semester = Column(Integer, nullable=False, default=1)
    credits = Column(Integer, nullable=False, default=0)
    is_active = Column(Boolean, nullable=False, default=True)


class FacultySubject(Base, ModelMixin):
    __tablename__ = 'faculty_subjects'

    id = Column(Integer, primary_key=True)
    faculty_id = Column(Integer, ForeignKey('faculty.id'), nullable=False)
    subject_id = Column(Integer, ForeignKey('subjects.id'), nullable=False)
    class_id = Column(Integer, ForeignKey('classes.id'), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
