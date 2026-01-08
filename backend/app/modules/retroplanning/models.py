
from datetime import datetime, date
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel

# --- Work Backwards Escolar/Universitario ---
class SchoolProjectBase(SQLModel):
    title: str
    vision: str  # Visión del proyecto
    press_release: str  # Press Release simulado
    faqs: List[str] = []  # Preguntas frecuentes
    roadmap: Optional[str] = None  # Roadmap general
    final_deadline: date
    created_at: datetime = Field(default_factory=datetime.utcnow)

class SchoolProject(SchoolProjectBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tasks: List["SchoolTask"] = Relationship(back_populates="project", cascade_delete=True)

class SchoolProjectCreate(SchoolProjectBase):
    pass

class SchoolProjectRead(SchoolProjectBase):
    id: int

class SchoolTaskBase(SQLModel):
    title: str
    description: Optional[str] = None
    responsible: Optional[str] = "Tú"
    duration_days: int = 1
    internal_deadline: date
    status: str = "pending" # pending, in_progress, completed

class SchoolTask(SchoolTaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="schoolproject.id")
    project: SchoolProject = Relationship(back_populates="tasks")

class SchoolTaskCreate(SchoolTaskBase):
    project_id: int

class SchoolTaskRead(SchoolTaskBase):
    id: int
    project_id: int

class SchoolTaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    responsible: Optional[str] = None
    duration_days: Optional[int] = None
    internal_deadline: Optional[date] = None
    status: Optional[str] = None

class SchoolProjectWithTasks(SchoolProjectRead):
    tasks: List[SchoolTaskRead] = []
