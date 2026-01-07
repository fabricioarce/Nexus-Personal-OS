from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class EisenhowerTask(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    urgency: int = Field(default=5, ge=1, le=10)
    importance: int = Field(default=5, ge=1, le=10)
    notes: Optional[str] = Field(default=None)
    status: str = Field(default="pending")  # pending, completed, archived
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class EisenhowerTaskCreate(SQLModel):
    title: str
    urgency: int = 5
    importance: int = 5
    notes: Optional[str] = None

class EisenhowerTaskRead(SQLModel):
    id: int
    title: str
    urgency: int
    importance: int
    notes: Optional[str]
    status: str
    created_at: datetime

class EisenhowerTaskUpdate(SQLModel):
    title: Optional[str] = None
    urgency: Optional[int] = None
    importance: Optional[int] = None
    notes: Optional[str] = None
    status: Optional[str] = None
