from backend.app.modules.profile.service import Profile
from backend.app.core.database import get_db
from sqlalchemy.orm import Session

class ProfileProvider:
    @staticmethod
    def get_profile(profile_id: int, db: Session = get_db()):
        return db.query(Profile).filter(Profile.id == profile_id).first()

    @staticmethod
    def get_profile_dict(profile_id: int, db: Session = get_db()):
        profile = db.query(Profile).filter(Profile.id == profile_id).first()
        if profile:
            return {
                "id": profile.id,
                "name": profile.name,
                "email": profile.email,
                "preferences": profile.preferences
            }
        return None
