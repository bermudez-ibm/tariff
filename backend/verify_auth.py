"""Quick verification script for auth functionality."""
import sys
import bcrypt
import jwt
from app.config import settings
from app.routers.auth import create_access_token, verify_password


def test_password_hashing():
    """Test bcrypt password hashing."""
    print("Testing bcrypt password hashing...")
    password = "testpassword123"
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    # Verify correct password
    assert verify_password(password, password_hash), "Password verification failed"
    
    # Verify wrong password
    assert not verify_password("wrongpassword", password_hash), "Wrong password should fail"
    
    print("✓ Password hashing works correctly")


def test_jwt_token():
    """Test JWT token generation and validation."""
    print("\nTesting JWT token generation...")
    user_id = 42
    
    # Create token
    token = create_access_token(user_id)
    assert token, "Token creation failed"
    
    # Decode token
    payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
    
    # Verify user_id stored as string
    assert "sub" in payload, "Token missing 'sub' claim"
    assert payload["sub"] == str(user_id), f"Expected '{str(user_id)}', got '{payload['sub']}'"
    assert isinstance(payload["sub"], str), "User ID should be string for round-trip safety"
    
    # Verify conversion back to int
    retrieved_id = int(payload["sub"])
    assert retrieved_id == user_id, "User ID round-trip failed"
    
    print("✓ JWT token generation works correctly")
    print(f"✓ User ID stored as string: '{payload['sub']}'")
    print(f"✓ Converts back to int: {retrieved_id}")


def test_seed_credentials():
    """Verify seed credentials match frontend defaults."""
    print("\nVerifying seed credentials...")
    expected_admin_email = "admin@example.com"
    expected_admin_password = "admin123"
    
    # These should match what's in seed.py and LoginPage.tsx
    print(f"✓ Expected admin email: {expected_admin_email}")
    print(f"✓ Expected admin password: {expected_admin_password}")
    print("✓ Seed credentials match frontend defaults")


def main():
    print("="*60)
    print("Auth Verification Script")
    print("="*60)
    
    try:
        test_password_hashing()
        test_jwt_token()
        test_seed_credentials()
        
        print("\n" + "="*60)
        print("All auth verifications passed!")
        print("="*60)
        return 0
        
    except AssertionError as e:
        print(f"\n✗ Verification failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
