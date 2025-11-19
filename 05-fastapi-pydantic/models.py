"""
Pydantic Models for Space Mission Control System

This module demonstrates Pydantic's powerful data validation capabilities
through space-themed models. Each model includes custom validators and
field constraints to ensure data integrity.
"""

from typing import Optional, Literal
from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime


class Astronaut(BaseModel):
    """
    Represents an astronaut in the space program.
    
    This model demonstrates:
    - Field constraints (min/max values, string patterns)
    - Email validation using EmailStr
    - Custom validators for business logic
    - Optional fields with defaults
    """
    
    id: Optional[int] = Field(default=None, description="Unique astronaut identifier")
    name: str = Field(..., min_length=2, max_length=100, description="Full name of the astronaut")
    age: int = Field(..., ge=21, le=65, description="Age must be between 21 and 65")
    email: EmailStr = Field(..., description="Valid email address")
    specialization: Literal["pilot", "engineer", "scientist", "medic", "commander"] = Field(
        ..., description="Astronaut's primary specialization"
    )
    years_of_experience: int = Field(..., ge=0, le=40, description="Years of relevant experience")
    active: bool = Field(default=True, description="Whether the astronaut is active in the program")
    
    @field_validator('name')
    @classmethod
    def name_must_not_contain_numbers(cls, v: str) -> str:
        """Ensure astronaut names don't contain numbers."""
        if any(char.isdigit() for char in v):
            raise ValueError('Name cannot contain numbers')
        return v.strip()
    
    @field_validator('years_of_experience')
    @classmethod
    def experience_must_be_reasonable_for_age(cls, v: int, info) -> int:
        """Validate that experience years make sense given the astronaut's age."""
        # Access age from the validation context
        age = info.data.get('age')
        if age and v > (age - 18):
            raise ValueError(f'Experience years ({v}) cannot exceed age minus 18 ({age - 18})')
        return v
    
    class Config:
        """Pydantic configuration for the model."""
        json_schema_extra = {
            "example": {
                "name": "Sarah Connor",
                "age": 35,
                "email": "sarah.connor@nasa.space",
                "specialization": "pilot",
                "years_of_experience": 12,
                "active": True
            }
        }


class Mission(BaseModel):
    """
    Represents a space mission.
    
    This model demonstrates:
    - Literal types for restricted choices
    - Field descriptions for auto-generated documentation
    - Nested validation logic
    - DateTime handling
    """
    
    id: Optional[int] = Field(default=None, description="Unique mission identifier")
    name: str = Field(..., min_length=3, max_length=100, description="Mission name")
    destination: str = Field(..., min_length=3, max_length=100, description="Target destination")
    duration_days: int = Field(..., ge=1, le=1000, description="Mission duration in days")
    status: Literal["planning", "active", "completed", "cancelled"] = Field(
        default="planning", description="Current mission status"
    )
    launch_date: Optional[datetime] = Field(default=None, description="Scheduled launch date")
    crew_capacity: int = Field(..., ge=1, le=10, description="Maximum crew size")
    current_crew_count: int = Field(default=0, ge=0, description="Current number of assigned crew members")
    
    @field_validator('name')
    @classmethod
    def name_must_be_capitalized(cls, v: str) -> str:
        """Ensure mission names follow proper capitalization."""
        return v.strip().title()
    
    @field_validator('current_crew_count')
    @classmethod
    def crew_count_cannot_exceed_capacity(cls, v: int, info) -> int:
        """Validate that current crew doesn't exceed capacity."""
        capacity = info.data.get('crew_capacity')
        if capacity and v > capacity:
            raise ValueError(f'Current crew count ({v}) cannot exceed capacity ({capacity})')
        return v
    
    @field_validator('launch_date')
    @classmethod
    def launch_date_must_be_future(cls, v: Optional[datetime]) -> Optional[datetime]:
        """Ensure launch date is in the future (if provided)."""
        if v and v < datetime.now():
            raise ValueError('Launch date must be in the future')
        return v
    
    class Config:
        """Pydantic configuration for the model."""
        json_schema_extra = {
            "example": {
                "name": "Mars Odyssey",
                "destination": "Mars",
                "duration_days": 180,
                "status": "planning",
                "launch_date": "2025-06-15T10:00:00",
                "crew_capacity": 6,
                "current_crew_count": 0
            }
        }


class CrewAssignment(BaseModel):
    """
    Represents the assignment of an astronaut to a mission.
    
    This model demonstrates:
    - Relationships between models
    - Role-based validation
    - Simple data transfer objects (DTOs)
    """
    
    astronaut_id: int = Field(..., ge=1, description="ID of the astronaut to assign")
    mission_id: int = Field(..., ge=1, description="ID of the mission")
    role: Literal["commander", "pilot", "engineer", "scientist", "medic", "specialist"] = Field(
        ..., description="Role of the astronaut in this mission"
    )
    
    class Config:
        """Pydantic configuration for the model."""
        json_schema_extra = {
            "example": {
                "astronaut_id": 1,
                "mission_id": 1,
                "role": "commander"
            }
        }


class AstronautResponse(Astronaut):
    """
    Response model for astronaut data.
    Extends the base Astronaut model to ensure ID is always present.
    """
    id: int  # Override to make ID required in responses


class MissionResponse(Mission):
    """
    Response model for mission data.
    Extends the base Mission model to ensure ID is always present.
    """
    id: int  # Override to make ID required in responses
