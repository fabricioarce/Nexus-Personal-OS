from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from backend.app.core.database import get_session
from .models import ProfileRead, ProfileCreate, ProfileUpdate
from .service import ProfileService

router = APIRouter()

@router.get("/", response_model=ProfileRead)
def get_profile(session: Session = Depends(get_session)):
    """Get the user profile"""
    profile = ProfileService.get_profile(session)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.post("/", response_model=ProfileRead)
def create_profile(profile: ProfileCreate, session: Session = Depends(get_session)):
    """Create a new profile"""
    try:
        return ProfileService.create_profile(session, profile)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/", response_model=ProfileRead)
def update_profile(profile: ProfileUpdate, session: Session = Depends(get_session)):
    """Update the user profile"""
    db_profile = ProfileService.update_profile(session, profile)
    if not db_profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return db_profile
