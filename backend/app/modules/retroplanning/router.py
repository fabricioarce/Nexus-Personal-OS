from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from backend.app.core.database import get_session
from backend.app.modules.retroplanning import models, service

router = APIRouter()

# --- Endpoints para proyectos escolares/universitarios ---
@router.post("/projects", response_model=models.SchoolProjectRead)
def create_project(project: models.SchoolProjectCreate, session: Session = Depends(get_session)):
    return service.create_project(session, project)

@router.get("/projects", response_model=List[models.SchoolProjectRead])
def read_projects(session: Session = Depends(get_session)):
    return service.get_projects(session)

@router.get("/projects/{project_id}", response_model=models.SchoolProjectWithTasks)
def read_project(project_id: int, session: Session = Depends(get_session)):
    project = service.get_project(session, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.delete("/projects/{project_id}")
def delete_project(project_id: int, session: Session = Depends(get_session)):
    # Implementar delete_project si es necesario
    return {"message": "Project deleted (implementación pendiente)"}

@router.post("/projects/{project_id}/tasks", response_model=models.SchoolTaskRead)
def create_task(project_id: int, task: models.SchoolTaskCreate, session: Session = Depends(get_session)):
    if task.project_id != project_id:
        raise HTTPException(status_code=400, detail="Project ID mismatch")
    return service.create_task(session, task)

@router.patch("/tasks/{task_id}", response_model=models.SchoolTaskRead)
def update_task(task_id: int, task: models.SchoolTaskUpdate, session: Session = Depends(get_session)):
    updated_task = service.update_task(session, task_id, task)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, session: Session = Depends(get_session)):
    if not service.delete_task(session, task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted"}
