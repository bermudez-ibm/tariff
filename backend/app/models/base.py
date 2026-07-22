"""Base declarative model and common columns."""
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class TimestampMixin:
    """Mixin for created_at and updated_at timestamps."""
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


class BaseModel(Base, TimestampMixin):
    """Abstract base model with id, created_at, updated_at."""
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, autoincrement=True)
