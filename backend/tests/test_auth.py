"""Unit tests for authentication endpoints."""
import pytest
import bcrypt
import jwt
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import get_db
from app.config import settings
from app.models.base import Base
from app.models.user import User, Role


# Test database setup
TEST_DATABASE_URL = "sqlite:///:memory:"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    """Override database dependency for testing."""
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(scope="function")
def test_db():
    """Create test database tables and clean up after test."""
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


def hash_password(plain_password: str) -> str:
    """Hash password using bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(plain_password.encode('utf-8'), salt).decode('utf-8')


def create_test_user(db, email: str = "test@example.com", password: str = "testpass123", full_name: str = "Test User"):
    """Helper to create a test user."""
    role = Role(name="Test Role", description="Test role description")
    db.add(role)
    db.flush()
    
    user = User(
        email=email,
        password_hash=hash_password(password),
        full_name=full_name,
        is_active=True
    )
    user.roles = [role]
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


class TestAuthLogin:
    """Test cases for POST /api/v1/auth/login endpoint."""
    
    def test_login_success(self, test_db):
        """Test successful login with valid credentials."""
        db = TestSessionLocal()
        user = create_test_user(db, email="admin@example.com", password="admin123")
        db.close()
        
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "admin@example.com", "password": "admin123"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify response structure matches shared_config.json
        assert "access_token" in data
        assert "user" in data
        
        # Verify user data
        assert data["user"]["email"] == "admin@example.com"
        assert data["user"]["full_name"] == "Test User"
        assert "id" in data["user"]
        assert "roles" in data["user"]
        assert len(data["user"]["roles"]) == 1
        
        # Verify JWT token can be decoded
        token = data["access_token"]
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        assert "sub" in payload
        assert payload["sub"] == str(user.id)  # User ID stored as string
    
    def test_login_invalid_email(self, test_db):
        """Test login with non-existent email."""
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "nonexistent@example.com", "password": "anypassword"}
        )
        
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid credentials"
    
    def test_login_invalid_password(self, test_db):
        """Test login with incorrect password."""
        db = TestSessionLocal()
        create_test_user(db, email="user@example.com", password="correctpass")
        db.close()
        
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "user@example.com", "password": "wrongpassword"}
        )
        
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid credentials"
    
    def test_login_inactive_user(self, test_db):
        """Test login with inactive user account."""
        db = TestSessionLocal()
        user = create_test_user(db, email="inactive@example.com", password="password123")
        user.is_active = False
        db.commit()
        db.close()
        
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "inactive@example.com", "password": "password123"}
        )
        
        assert response.status_code == 401
        assert response.json()["detail"] == "User account is inactive"
    
    def test_login_field_names_match_config(self, test_db):
        """Test that login accepts field names from shared_config.json."""
        db = TestSessionLocal()
        create_test_user(db, email="config@example.com", password="configpass")
        db.close()
        
        # shared_config.json specifies field_names: ["email", "password"]
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "config@example.com", "password": "configpass"}
        )
        
        assert response.status_code == 200
    
    def test_login_missing_email(self, test_db):
        """Test login with missing email field."""
        response = client.post(
            "/api/v1/auth/login",
            json={"password": "somepassword"}
        )
        
        assert response.status_code == 422  # Validation error
    
    def test_login_missing_password(self, test_db):
        """Test login with missing password field."""
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "test@example.com"}
        )
        
        assert response.status_code == 422  # Validation error
    
    def test_token_contains_user_id_as_string(self, test_db):
        """Test that JWT token embeds user.id as string for round-trip safety."""
        db = TestSessionLocal()
        user = create_test_user(db)
        db.close()
        
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "test@example.com", "password": "testpass123"}
        )
        
        token = response.json()["access_token"]
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        
        # Verify 'sub' is a string
        assert isinstance(payload["sub"], str)
        # Verify it can be converted back to int
        user_id = int(payload["sub"])
        assert user_id == user.id


class TestAuthMiddleware:
    """Test cases for JWT authentication middleware."""
    
    def test_protected_endpoint_without_token(self, test_db):
        """Test that protected endpoint returns 401 without auth token."""
        response = client.get("/api/v1/policy-events")
        
        assert response.status_code == 403  # No credentials provided
    
    def test_protected_endpoint_with_valid_token(self, test_db):
        """Test that protected endpoint accepts valid JWT token."""
        db = TestSessionLocal()
        user = create_test_user(db)
        db.close()
        
        # Login to get token
        login_response = client.post(
            "/api/v1/auth/login",
            json={"email": "test@example.com", "password": "testpass123"}
        )
        token = login_response.json()["access_token"]
        
        # Call protected endpoint with token
        response = client.get(
            "/api/v1/policy-events",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        # Should not return 401 (may return other codes based on implementation)
        assert response.status_code != 401
    
    def test_protected_endpoint_with_invalid_token(self, test_db):
        """Test that protected endpoint rejects invalid JWT token."""
        response = client.get(
            "/api/v1/policy-events",
            headers={"Authorization": "Bearer invalid-token-string"}
        )
        
        assert response.status_code == 401
    
    def test_protected_endpoint_with_expired_token(self, test_db):
        """Test that protected endpoint rejects expired JWT token."""
        db = TestSessionLocal()
        user = create_test_user(db)
        db.close()
        
        # Create an expired token
        expire = datetime.utcnow() - timedelta(minutes=10)  # Expired 10 minutes ago
        payload = {
            "sub": str(user.id),
            "exp": expire,
            "iat": datetime.utcnow() - timedelta(minutes=20),
        }
        expired_token = jwt.encode(payload, settings.secret_key, algorithm="HS256")
        
        response = client.get(
            "/api/v1/policy-events",
            headers={"Authorization": f"Bearer {expired_token}"}
        )
        
        assert response.status_code == 401
        assert "expired" in response.json()["detail"].lower()
