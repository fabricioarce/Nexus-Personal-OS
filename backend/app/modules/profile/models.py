from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class UserProfile(SQLModel, table=True):
    """User profile model with personal information for psychological analysis"""
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Basic Information
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)
    birth_year: Optional[int] = Field(default=None)
    
    # Location
    city: Optional[str] = Field(default=None)
    country: Optional[str] = Field(default=None)
    timezone: Optional[str] = Field(default=None)
    
    # Physical Data
    height_cm: Optional[int] = Field(default=None)  # Height in centimeters
    weight_kg: Optional[float] = Field(default=None)  # Weight in kilograms
    
    # Additional Information
    occupation: Optional[str] = Field(default=None)
    education_level: Optional[str] = Field(default=None)
    marital_status: Optional[str] = Field(default=None)
    
    # Open notes for additional information
    additional_notes: Optional[str] = Field(default=None)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ProfileCreate(SQLModel):
    """Schema for creating a profile"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birth_year: Optional[int] = None
    city: Optional[str] = None
    country: Optional[str] = None
    timezone: Optional[str] = None
    height_cm: Optional[int] = None
    weight_kg: Optional[float] = None
    occupation: Optional[str] = None
    education_level: Optional[str] = None
    marital_status: Optional[str] = None
    additional_notes: Optional[str] = None

class ProfileRead(SQLModel):
    """Schema for reading a profile"""
    id: int
    first_name: Optional[str]
    last_name: Optional[str]
    birth_year: Optional[int]
    age: Optional[int] = None  # Calculated field
    city: Optional[str]
    country: Optional[str]
    timezone: Optional[str]
    height_cm: Optional[int]
    weight_kg: Optional[float]
    occupation: Optional[str]
    education_level: Optional[str]
    marital_status: Optional[str]
    additional_notes: Optional[str]
    created_at: datetime
    updated_at: datetime

class ProfileUpdate(SQLModel):
    """Schema for updating a profile"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birth_year: Optional[int] = None
    city: Optional[str] = None
    country: Optional[str] = None
    timezone: Optional[str] = None
    height_cm: Optional[int] = None
    weight_kg: Optional[float] = None
    occupation: Optional[str] = None
    education_level: Optional[str] = None
    marital_status: Optional[str] = None
    additional_notes: Optional[str] = None
