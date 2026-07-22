#!/usr/bin/env python3
"""Quick login verification script for Tariff Resilience API."""
import json
import sys
import urllib.request
from urllib.error import HTTPError, URLError


def test_login(base_url: str = "http://localhost:19000", email: str = "admin@example.com", password: str = "admin123"):
    """Test login and protected endpoint access."""
    
    print(f"Testing Tariff Resilience API at {base_url}")
    print("=" * 60)
    
    # Test 1: Health check
    try:
        resp = urllib.request.urlopen(f"{base_url}/health")
        health = json.loads(resp.read().decode())
        print(f"✓ Health check: {health.get('status')}")
    except Exception as e:
        print(f"✗ Health check failed: {e}")
        return False
    
    # Test 2: Login
    try:
        url = f"{base_url}/api/v1/auth/login"
        data = json.dumps({"email": email, "password": password}).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        resp = urllib.request.urlopen(req)
        login_result = json.loads(resp.read().decode())
        token = login_result.get("access_token")
        user = login_result.get("user", {})
        print(f"✓ Login successful: {user.get('email')}")
        print(f"  Roles: {', '.join(user.get('roles', []))}")
    except HTTPError as e:
        print(f"✗ Login failed with HTTP {e.code}: {e.reason}")
        return False
    except Exception as e:
        print(f"✗ Login failed: {e}")
        return False
    
    # Test 3: Protected endpoint
    try:
        url = f"{base_url}/api/v1/dashboard/exposure?role=Executive"
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
        resp = urllib.request.urlopen(req)
        dashboard = json.loads(resp.read().decode())
        print(f"✓ Protected endpoint access successful")
        print(f"  Exposure data keys: {', '.join(list(dashboard.keys())[:5])}")
    except HTTPError as e:
        print(f"✗ Protected endpoint failed with HTTP {e.code}: {e.reason}")
        return False
    except Exception as e:
        print(f"✗ Protected endpoint failed: {e}")
        return False
    
    print("=" * 60)
    print("✓ All tests passed!")
    return True


if __name__ == "__main__":
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:19000"
    success = test_login(base_url)
    sys.exit(0 if success else 1)
