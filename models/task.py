from sqlalchemy import Column, Integer, SmallInteger, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from database import Base

from enum import Enum as EnumPy


class Status(EnumPy):
    pending = 'pending'
    completed = 'completed'


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(75), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(20), default='pending', nullable=False)
    is_active = Column(SmallInteger, default=1, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relacion muchos a muchos con Tag
    tags = relationship('Tag', secondary='task_tags', back_populates='tasks')
