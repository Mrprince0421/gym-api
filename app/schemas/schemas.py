from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator
from app.models.models import UserRole

class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=72)
    role: UserRole = UserRole.MEMBER
    full_name: Optional[str] = Field(None, min_length=3, max_length=150)
    phone: Optional[str] = Field(None, max_length=20)
    plan_name: str = Field("Mensal", max_length=50)

    @field_validator("password")
    @classmethod
    def strong_password(cls, v: str) -> str:
        if not any(c.isdigit() for c in v) or not any(c.isalpha() for c in v):
            raise ValueError("A senha deve conter letras e números.")
        return v

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class MemberCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=72)
    full_name: str = Field(..., min_length=3, max_length=150)
    phone: Optional[str] = Field(None, max_length=20)
    plan_name: str = Field("Mensal", max_length=50)

class MemberOut(BaseModel):
    id: int
    user_id: int
    full_name: str
    phone: Optional[str]
    plan_name: str
    active: bool
    joined_at: datetime

    class Config:
        from_attributes = True

class WorkoutCreate(BaseModel):
    member_id: int = Field(..., gt=0)
    title: str = Field(..., min_length=3, max_length=120)
    description: str = Field(..., min_length=5, max_length=2000)

class WorkoutOut(BaseModel):
    id: int
    member_id: int
    trainer_id: Optional[int]
    title: str
    description: str
    created_at: datetime

    class Config:
        from_attributes = True

class CheckInCreate(BaseModel):
    member_id: int = Field(..., gt=0)

class CheckInOut(BaseModel):
    id: int
    member_id: int
    checked_in_at: datetime

    class Config:
        from_attributes = True