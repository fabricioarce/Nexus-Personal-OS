
from datetime import datetime, date
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel

class RetroProjectBase(SQLModel):
    title: str
    description: Optional[str] = None
    final_deadline: date
    created_at: datetime = Field(default_factory=datetime.utcnow)

class RetroProject(RetroProjectBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tasks: List["RetroTask"] = Relationship(back_populates="project", cascade_delete=True)

class RetroProjectCreate(RetroProjectBase):
    pass

class RetroProjectRead(RetroProjectBase):
    id: int

class RetroTaskBase(SQLModel):
    title: str
    description: Optional[str] = None
    responsible: Optional[str] = "Tú"
    duration_days: int = 1
    internal_deadline: date
    status: str = "pending" # pending, completed

class RetroTask(RetroTaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="retroproject.id")
    project: RetroProject = Relationship(back_populates="tasks")

class RetroTaskCreate(RetroTaskBase):
    project_id: int

class RetroTaskRead(RetroTaskBase):
    id: int
    project_id: int

class RetroTaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    responsible: Optional[str] = None
    duration_days: Optional[int] = None
    internal_deadline: Optional[date] = None
    status: Optional[str] = None

class RetroProjectWithTasks(RetroProjectRead):
    tasks: List[RetroTaskRead] = []
