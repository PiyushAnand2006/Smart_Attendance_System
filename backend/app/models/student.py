"""Student & Parent Models."""
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from app.db import Base, ModelMixin


class Student(Base, ModelMixin):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    student_id = Column(String(32), unique=True, nullable=False)
    first_name = Column(String(64), nullable=False, default='')
    last_name = Column(String(64), nullable=False, default='')
    roll_number = Column(String(32), nullable=True)
    class_id = Column(Integer, ForeignKey('classes.id'), nullable=True)
    section = Column(String(16), nullable=True)
    department = Column(String(64), nullable=True)
    enrollment_status = Column(String(32), nullable=False, default='incomplete')
    is_active = Column(Boolean, nullable=False, default=True)

    def to_dict(self, exclude=None):
        d = super().to_dict(exclude=exclude or set())
        d['full_name'] = f"{self.first_name or ''} {self.last_name or ''}".strip()
        return d


class ParentGuardian(Base, ModelMixin):
    __tablename__ = 'parents'

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False, index=True)
    name = Column(String(120), nullable=True)
    whatsapp_number = Column(String(32), nullable=True)
    relationship = Column(String(32), nullable=True, default='father')
