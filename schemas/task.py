from pydantic import BaseModel, Field

from datetime import datetime
from typing import Optional, List
from enum import Enum

class Status(Enum):
    pending = 'pending'
    completed = 'completed'


class TaskBase(BaseModel):
    title: str = Field(min_length=3, max_length=75)
    description: Optional[str]
    status: Status 


class TaskRead(TaskBase):
    id: int
    created_at: datetime
    tag_count: int = 0

    class Config:
        from_attributes = True


class TaskCreate(TaskBase):
    tag_names: Optional[List[str]] = Field(default=[], description="Nombres de las etiquetas a asociar")


class TaskUpdate(TaskBase):
    tag_names: Optional[List[str]] = Field(default=None, description="Nombres de las etiquetas a asociar")
