"""Face Recognition Models."""
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text

from app.db import Base, ModelMixin


class FaceEmbedding(Base, ModelMixin):
    __tablename__ = 'face_embeddings'

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False, unique=True)
    embedding = Column(Text, nullable=True)
    samples = Column(Integer, nullable=False, default=0)
    is_active = Column(Boolean, nullable=False, default=True)
