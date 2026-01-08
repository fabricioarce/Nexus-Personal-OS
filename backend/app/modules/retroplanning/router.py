from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from backend.app.core.database import get_session
from backend.app.modules.retroplanning import models, service

router = APIRouter()

@router.post("/projects", response_model=models.RetroProjectRead)
def create_project(project: models.RetroProjectCreate, session: Session = Depends(get_session)):
    return service.create_project(session, project)

@router.get("/projects", response_model=List[models.RetroProjectRead])
def read_projects(session: Session = Depends(get_session)):
    return service.get_projects(session)

@router.get("/projects/{project_id}", response_model=models.RetroProjectWithTasks)
def read_project(project_id: int, session: Session = Depends(get_session)):
    project = service.get_project(session, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.delete("/projects/{project_id}")
def delete_project(project_id: int, session: Session = Depends(get_session)):
    if not service.delete_project(session, project_id):
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": "Project deleted"}

@router.post("/projects/{project_id}/tasks", response_model=models.RetroTaskRead)
def create_task(project_id: int, task: models.RetroTaskCreate, session: Session = Depends(get_session)):
    if task.project_id != project_id:
        raise HTTPException(status_code=400, detail="Project ID mismatch")
    return service.create_task(session, task)

@router.patch("/tasks/{task_id}", response_model=models.RetroTaskRead)
def update_task(task_id: int, task: models.RetroTaskUpdate, session: Session = Depends(get_session)):
    updated_task = service.update_task(session, task_id, task)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, session: Session = Depends(get_session)):
    if not service.delete_task(session, task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted"}
