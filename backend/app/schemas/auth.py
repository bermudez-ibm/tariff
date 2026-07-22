"""Authentication schemas."""
from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    """Login request payload."""
    email: EmailStr
    password: str = Field(..., min_length=1)


class UserResponse(BaseModel):
    """User response data."""
    id: int
    email: str
    name: str
    
    model_config = {'from_attributes': True}


class LoginResponse(BaseModel):
    """Login response payload."""
    access_token: str
    user: UserResponse
