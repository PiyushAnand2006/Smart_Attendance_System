"""User Model (admin / faculty / student)."""
from sqlalchemy import Boolean, Column, Integer, String

from app.db import Base, ModelMixin


class User(Base, ModelMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    user_id = Column(String(32), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False, index=True)
    password = Column(String(128), nullable=False)
    first_name = Column(String(64), nullable=False, default='')
    last_name = Column(String(64), nullable=False, default='')
    role = Column(String(20), nullable=False, default='student')
    is_active = Column(Boolean, nullable=False, default=True)

    def to_dict(self, exclude=None):
        # Never leak the password hash.
        return super().to_dict(exclude=(exclude or set()) | {'password'})
