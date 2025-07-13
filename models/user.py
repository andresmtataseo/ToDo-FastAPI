from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from database import Base


class User(Base):
    __tablename__ = 'users'

    # Columnas de la tabla
    id = Column(Integer, primary_key=True)
    name = Column(String(75), nullable=False)
    email = Column(String(127), nullable=False)
    password = Column(String(127), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
