from typing import List, Optional
from sqlmodel import Session, select
from datetime import datetime
from .models import EisenhowerTask, EisenhowerTaskCreate, EisenhowerTaskUpdate

class EisenhowerService:
    @staticmethod
    def create_task(session: Session, task_data: EisenhowerTaskCreate) -> EisenhowerTask:
        db_task = EisenhowerTask.from_orm(task_data)
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task

    @staticmethod
    def get_tasks(session: Session, include_completed: bool = False) -> List[EisenhowerTask]:
        statement = select(EisenhowerTask)
        if not include_completed:
            statement = statement.where(EisenhowerTask.status != "completed")
        results = session.exec(statement)
        return results.all()

    @staticmethod
    def get_task(session: Session, task_id: int) -> Optional[EisenhowerTask]:
        return session.get(EisenhowerTask, task_id)

    @staticmethod
    def update_task(session: Session, task_id: int, task_data: EisenhowerTaskUpdate) -> Optional[EisenhowerTask]:
        db_task = session.get(EisenhowerTask, task_id)
        if not db_task:
            return None
        
        data = task_data.dict(exclude_unset=True)
        for key, value in data.items():
            setattr(db_task, key, value)
        
        db_task.updated_at = datetime.utcnow()
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task

    @staticmethod
    def delete_task(session: Session, task_id: int) -> bool:
        db_task = session.get(EisenhowerTask, task_id)
        if not db_task:
            return False
        session.delete(db_task)
        session.commit()
        return True
