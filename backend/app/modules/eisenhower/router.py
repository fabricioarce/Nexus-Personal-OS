from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from backend.app.core.database import get_session
from .models import EisenhowerTaskRead, EisenhowerTaskCreate, EisenhowerTaskUpdate
from .service import EisenhowerService

router = APIRouter()

@router.post("/", response_model=EisenhowerTaskRead)
def create_task(task: EisenhowerTaskCreate, session: Session = Depends(get_session)):
    return EisenhowerService.create_task(session, task)

@router.get("/", response_model=List[EisenhowerTaskRead])
def get_tasks(include_completed: bool = False, session: Session = Depends(get_session)):
    return EisenhowerService.get_tasks(session, include_completed)

@router.get("/{task_id}", response_model=EisenhowerTaskRead)
def get_task(task_id: int, session: Session = Depends(get_session)):
    db_task = EisenhowerService.get_task(session, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.patch("/{task_id}", response_model=EisenhowerTaskRead)
def update_task(task_id: int, task: EisenhowerTaskUpdate, session: Session = Depends(get_session)):
    db_task = EisenhowerService.update_task(session, task_id, task)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.delete("/{task_id}")
def delete_task(task_id: int, session: Session = Depends(get_session)):
    success = EisenhowerService.delete_task(session, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted"}
