from pydantic import BaseModel

class Profile(BaseModel):
    id: int
    name: str
    email: str
    preferences: dict = {}
