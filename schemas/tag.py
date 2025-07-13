from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class TagBase(BaseModel):
    name: str = Field(min_length=1, max_length=50, description="Nombre de la etiqueta")


class TagCreate(TagBase):
    pass


class TagUpdate(TagBase):
    pass


class TagRead(TagBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class TagWithTasks(TagRead):
    # Eliminamos la referencia circular por ahora
    task_count: int = 0 