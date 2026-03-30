from pydantic import BaseModel, Field, field_validator
from typing import Optional

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    weight: float = Field(..., gt=20, lt=300)
    height: float = Field(..., gt=100, lt=250)
    target_calories: int = Field(..., gt=500, lt=10000)

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True