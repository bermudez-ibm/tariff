"""Authentication router for JWT token generation."""
from datetime import datetime, timedelta
from typing import Optional

import bcrypt
import jwt
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models.user import User


router = APIRouter(prefix="/auth", tags=["auth"])


# Request/Response schemas
class LoginRequest(BaseModel):
    """Login request matching shared_config.json field names."""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """User response model."""
    id: int
    email: str
    full_name: str
    roles: list[str]

    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    """Login response matching shared_config.json structure."""
    access_token: str
    user: UserResponse


def create_access_token(user_id: int, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token with user ID as string for round-trip safety."""
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.access_token_expire_minutes)
    
    expire = datetime.utcnow() + expires_delta
    payload = {
        "sub": str(user_id),  # String for round-trip type safety
        "exp": expire,
        "iat": datetime.utcnow(),
    }
    
    token = jwt.encode(payload, settings.secret_key, algorithm="HS256")
    return token


def verify_password(plain_password: str, password_hash: str) -> bool:
    """Verify password using bcrypt."""
    return bcrypt.checkpw(plain_password.encode('utf-8'), password_hash.encode('utf-8'))


@router.post("/login", response_model=LoginResponse)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate user and return JWT token.
    
    REQ-AUTH-001: JWT authentication with bcrypt password hashing.
    Field names match shared_config.json: email, password.
    Response matches shared_config.json: access_token, user.
    """
    # Find user by email
    user = db.query(User).filter(User.email == credentials.email).first()
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not user.is_active:
        raise HTTPException(status_code=401, detail="User account is inactive")
    
    # Verify password
    if not verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create JWT token
    access_token = create_access_token(user.id)
    
    # Build user response with roles
    role_names = [role.name for role in user.roles]
    user_response = UserResponse(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        roles=role_names
    )
    
    return LoginResponse(access_token=access_token, user=user_response)
