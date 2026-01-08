from sqlalchemy import Column, Integer, String, JSON
from ..core.database import Base

class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    preferences = Column(JSON, default={})
