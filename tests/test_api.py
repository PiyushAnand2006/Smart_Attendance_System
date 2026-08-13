"""Test the SmartAttend Backend API"""
import sys
import io
import requests

# Allow unicode checkmarks on Windows consoles (cp1252)
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

BASE_URL = "http://localhost:5000"


def test_health():
    """Test health endpoint"""
    res = requests.get(f"{BASE_URL}/health")
    assert res.status_code == 200
    print("✓ Health check passed")


def test_login():
    """Test login endpoint"""
    res = requests.post(f"{BASE_URL}/api/auth/login",
                        json={"email": "admin@smartattend.com", "password": "admin123"})
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert "access_token" in data["data"]
    print("✓ Admin login passed")
    return data["data"]["access_token"]


def test_register():
    """Test registration endpoint (unique email per run)"""
    import uuid
    email = f"test_{uuid.uuid4().hex[:8]}@college.edu"
    res = requests.post(f"{BASE_URL}/api/auth/register",
                        json={"email": email, "password": "secret123",
                              "first_name": "Test", "last_name": "User", "role": "student"})
    assert res.status_code in (200, 201)
    print("✓ Registration passed")


def test_admin_dashboard(token):
    """Test admin dashboard"""
    res = requests.get(f"{BASE_URL}/api/admin/dashboard",
                       headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    data = res.json()
    assert "total_students" in data["data"]
    print("✓ Admin dashboard passed")


def test_students(token):
    """Test students endpoint"""
    res = requests.get(f"{BASE_URL}/api/students",
                       headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    print("✓ Students list passed")


def test_create_session(token):
    """Test creating an attendance session"""
    res = requests.post(f"{BASE_URL}/api/attendance/sessions",
                        headers={"Authorization": f"Bearer {token}"},
                        json={"subject_id": 1, "class_id": 1, "mode": "FACE"})
    assert res.status_code == 201
    print("✓ Create session passed")


def test_monthly_report(token):
    """Test monthly report"""
    res = requests.get(f"{BASE_URL}/api/reports/monthly",
                       headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    print("✓ Monthly report passed")


if __name__ == "__main__":
    print("\n=== SmartAttend API Tests ===\n")
    try:
        test_health()
        token = test_login()
        test_register()
        test_admin_dashboard(token)
        test_students(token)
        test_create_session(token)
        test_monthly_report(token)
        print("\n✅ All tests passed!\n")
    except Exception as e:
        print(f"\n❌ Test failed: {e}\n")
        raise
