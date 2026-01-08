from fastapi import APIRouter, HTTPException, status, Body
from .models import Profile
from ..core.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/profile", tags=["profile"])

@router.patch("/", response_model=Profile)
def update_profile(profile: Profile = Body(...), db: Session = get_db()):
    db_profile = db.query(Profile).filter(Profile.id == profile.id).first()
    if not db_profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    for key, value in profile.dict(exclude_unset=True).items():
        setattr(db_profile, key, value)
    db.commit()
    db.refresh(db_profile)
    return db_profile

@router.get("/{profile_id}", response_model=Profile)
def get_profile(profile_id: int, db: Session = get_db()):
    db_profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not db_profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return db_profile
