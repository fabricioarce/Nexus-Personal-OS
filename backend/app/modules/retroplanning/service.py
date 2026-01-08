def create_project(session: Session, project: RetroProjectCreate) -> RetroProject:
def get_projects(session: Session) -> List[RetroProject]:
def get_project(session: Session, project_id: int) -> Optional[RetroProject]:
def create_task(session: Session, task: RetroTaskCreate) -> RetroTask:
def update_task(session: Session, task_id: int, task_update: RetroTaskUpdate) -> Optional[RetroTask]:
def delete_task(session: Session, task_id: int) -> bool:
from sqlmodel import Session, select
from typing import List, Optional
from backend.app.modules.retroplanning.models import (
    SchoolProject, SchoolTask, SchoolProjectCreate, SchoolTaskCreate, SchoolTaskUpdate
)

def create_project(session: Session, project: SchoolProjectCreate) -> SchoolProject:
    db_project = SchoolProject.from_orm(project)
    session.add(db_project)
    session.commit()
    session.refresh(db_project)
    return db_project

def get_projects(session: Session) -> List[SchoolProject]:
    return session.exec(select(SchoolProject)).all()

def get_project(session: Session, project_id: int) -> Optional[SchoolProject]:
    return session.get(SchoolProject, project_id)

def create_task(session: Session, task: SchoolTaskCreate) -> SchoolTask:
    db_task = SchoolTask.from_orm(task)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

def update_task(session: Session, task_id: int, task_update: SchoolTaskUpdate) -> Optional[SchoolTask]:
    db_task = session.get(SchoolTask, task_id)
    if not db_task:
        return None
    task_data = task_update.dict(exclude_unset=True)
    for key, value in task_data.items():
        setattr(db_task, key, value)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

def delete_task(session: Session, task_id: int) -> bool:
    db_task = session.get(SchoolTask, task_id)
    if not db_task:
        return False
    session.delete(db_task)
    session.commit()
    return True

def delete_project(session: Session, project_id: int) -> bool:
    db_project = session.get(RetroProject, project_id)
    if not db_project:
        return False
    session.delete(db_project)
    session.commit()
    return True
