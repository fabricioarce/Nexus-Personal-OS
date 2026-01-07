from fastapi import APIRouter
from pydantic import BaseModel
from backend.app.services.diary_service import (
    save_entry,
    list_entries,
    read_entry,
)

router = APIRouter()

class DiaryEntry(BaseModel):
    text: str

@router.post("/save")
def save_diary(entry: DiaryEntry):
    save_entry(entry.text)
    return {"status": "ok"}

@router.get("/list")
def list_diary():
    return list_entries()

@router.get("/{date}")
def get_diary(date: str):
    return read_entry(date)
