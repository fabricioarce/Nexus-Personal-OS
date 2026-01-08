from datetime import datetime
from typing import Optional
from sqlmodel import Session, select
from .models import UserProfile, ProfileCreate, ProfileUpdate, ProfileRead

class ProfileService:
    """Service layer for profile operations"""
    
    @staticmethod
    def get_profile(session: Session) -> Optional[ProfileRead]:
        """Get the user profile (only one profile supported)"""
        statement = select(UserProfile)
        profile = session.exec(statement).first()
        
        if not profile:
            return None
        
        # Convert to ProfileRead and add calculated age
        profile_data = profile.model_dump()
        profile_data['age'] = ProfileService.calculate_age(profile.birth_year) if profile.birth_year else None
        
        return ProfileRead(**profile_data)
    
    @staticmethod
    def create_profile(session: Session, profile_data: ProfileCreate) -> ProfileRead:
        """Create a new profile"""
        # Check if profile already exists
        existing = session.exec(select(UserProfile)).first()
        if existing:
            raise ValueError("Profile already exists. Use update instead.")
        
        db_profile = UserProfile(**profile_data.model_dump())
        session.add(db_profile)
        session.commit()
        session.refresh(db_profile)
        
        # Convert to ProfileRead with calculated age
        result_data = db_profile.model_dump()
        result_data['age'] = ProfileService.calculate_age(db_profile.birth_year) if db_profile.birth_year else None
        
        return ProfileRead(**result_data)
    
    @staticmethod
    def update_profile(session: Session, profile_data: ProfileUpdate) -> Optional[ProfileRead]:
        """Update the existing profile"""
        statement = select(UserProfile)
        db_profile = session.exec(statement).first()
        
        if not db_profile:
            return None
        
        # Update only provided fields
        update_dict = profile_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(db_profile, key, value)
        
        db_profile.updated_at = datetime.utcnow()
        session.add(db_profile)
        session.commit()
        session.refresh(db_profile)
        
        # Convert to ProfileRead with calculated age
        result_data = db_profile.model_dump()
        result_data['age'] = ProfileService.calculate_age(db_profile.birth_year) if db_profile.birth_year else None
        
        return ProfileRead(**result_data)
    
    @staticmethod
    def calculate_age(birth_year: Optional[int]) -> Optional[int]:
        """Calculate age from birth year"""
        if birth_year is None:
            return None
        
        current_year = datetime.now().year
        return current_year - birth_year
