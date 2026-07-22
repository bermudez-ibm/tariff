"""User and authentication models."""
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from .base import BaseModel, Base

# Association table for many-to-many relationship between users and roles
user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True)
)


class User(BaseModel):
    """User model with Integer PK."""
    __tablename__ = 'users'
    
    email = Column(String(255), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    
    # Many-to-many relationship with roles
    roles = relationship('Role', secondary=user_roles, back_populates='users')


class Role(BaseModel):
    """Role model for RBAC."""
    __tablename__ = 'roles'
    
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(500))
    
    # Many-to-many relationship with users
    users = relationship('User', secondary=user_roles, back_populates='roles')
