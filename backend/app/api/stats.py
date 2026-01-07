# api/stats.py
from fastapi import APIRouter

router = APIRouter()

@router.get("")
def stats():
    # [Inferencia] aquí deberías devolver
    # algo como emociones por mes
    return {
        "ansiedad": 0.6,
        "alegria": 0.3,
        "neutral": 0.1,
    }
