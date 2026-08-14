"""Faculty Model."""
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from app.db import Base, ModelMixin


class Faculty(Base, ModelMixin):
    __tablename__ = 'faculty'

    id = Column(Integer, primary_key=True)
    faculty_id = Column(String(32), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    first_name = Column(String(64), nullable=False, default='')
    last_name = Column(String(64), nullable=False, default='')
    department = Column(String(64), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)

    def to_dict(self, exclude=None):
        d = super().to_dict(exclude=exclude or set())
        d['full_name'] = f"{self.first_name or ''} {self.last_name or ''}".strip()
        return d
