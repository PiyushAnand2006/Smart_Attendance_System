"""Class & Section Models."""
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from app.db import Base, ModelMixin


class ClassModel(Base, ModelMixin):
    __tablename__ = 'classes'

    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    code = Column(String(32), unique=True, nullable=False)
    department = Column(String(64), nullable=True)
    batch_year = Column(Integer, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)


class Section(Base, ModelMixin):
    __tablename__ = 'sections'

    id = Column(Integer, primary_key=True)
    class_id = Column(Integer, ForeignKey('classes.id'), nullable=False)
    name = Column(String(32), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
