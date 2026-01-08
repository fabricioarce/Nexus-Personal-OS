from sqlmodel import Session, select
from typing import List, Optional
from backend.app.modules.retroplanning.models import (
    RetroProject, RetroTask, RetroProjectCreate, RetroTaskCreate, RetroTaskUpdate
)

def create_project(session: Session, project: RetroProjectCreate) -> RetroProject:
    db_project = RetroProject.from_orm(project)
    session.add(db_project)
    session.commit()
    session.refresh(db_project)
    return db_project

def get_projects(session: Session) -> List[RetroProject]:
    return session.exec(select(RetroProject)).all()

def get_project(session: Session, project_id: int) -> Optional[RetroProject]:
    return session.get(RetroProject, project_id)

def create_task(session: Session, task: RetroTaskCreate) -> RetroTask:
    db_task = RetroTask.from_orm(task)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

def update_task(session: Session, task_id: int, task_update: RetroTaskUpdate) -> Optional[RetroTask]:
    db_task = session.get(RetroTask, task_id)
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
    db_task = session.get(RetroTask, task_id)
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
