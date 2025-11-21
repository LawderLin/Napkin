"""
API integration tests for Napkin backend
These tests require the backend server and PostgreSQL to be running
"""
import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_health_check():
    """Test the health check endpoint"""
    response = requests.get(f"{BASE_URL}/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    print("✓ Health check passed")

def test_create_note():
    """Test creating a note"""
    data = {
        "content": "# Test Note\n\nThis is a test note with **markdown**."
    }
    response = requests.post(f"{BASE_URL}/api/notes", json=data)
    assert response.status_code == 201
    assert "id" in response.json()
    note_id = response.json()["id"]
    print(f"✓ Note created with ID: {note_id}")
    return note_id

def test_get_note(note_id):
    """Test retrieving a note"""
    response = requests.get(f"{BASE_URL}/api/notes/{note_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == note_id
    assert "content" in data
    assert data["views"] == 1
    print(f"✓ Note retrieved successfully")
    return data

def test_check_note(note_id):
    """Test checking note status"""
    response = requests.get(f"{BASE_URL}/api/notes/{note_id}/check")
    assert response.status_code == 200
    data = response.json()
    assert data["exists"] == True
    assert "requires_password" in data
    print(f"✓ Note check passed")

def test_password_protected_note():
    """Test creating and accessing a password-protected note"""
    data = {
        "content": "Secret note",
        "password": "secret123"
    }
    response = requests.post(f"{BASE_URL}/api/notes", json=data)
    assert response.status_code == 201
    note_id = response.json()["id"]
    
    # Try accessing without password
    response = requests.get(f"{BASE_URL}/api/notes/{note_id}")
    assert response.status_code == 403
    
    # Try with wrong password
    response = requests.get(f"{BASE_URL}/api/notes/{note_id}?password=wrong")
    assert response.status_code == 403
    
    # Try with correct password
    response = requests.get(f"{BASE_URL}/api/notes/{note_id}?password=secret123")
    assert response.status_code == 200
    
    print(f"✓ Password protection works correctly")
    return note_id

def test_expiring_note():
    """Test creating a note with expiration"""
    data = {
        "content": "Expiring note",
        "expire_hours": 1
    }
    response = requests.post(f"{BASE_URL}/api/notes", json=data)
    assert response.status_code == 201
    assert "expires_at" in response.json()
    assert response.json()["expires_at"] is not None
    print(f"✓ Note expiration works correctly")

def test_delete_note(note_id):
    """Test deleting a note"""
    response = requests.delete(f"{BASE_URL}/api/notes/{note_id}")
    assert response.status_code == 200
    
    # Verify note is deleted
    response = requests.get(f"{BASE_URL}/api/notes/{note_id}")
    assert response.status_code == 404
    print(f"✓ Note deleted successfully")

def run_tests():
    """Run all API tests"""
    print("Running Napkin API Tests")
    print("========================\n")
    
    try:
        # Test health check
        test_health_check()
        
        # Test basic note creation and retrieval
        note_id = test_create_note()
        test_check_note(note_id)
        test_get_note(note_id)
        
        # Test password protection
        protected_note_id = test_password_protected_note()
        
        # Test expiration
        test_expiring_note()
        
        # Clean up - delete test notes
        test_delete_note(note_id)
        test_delete_note(protected_note_id)
        
        print("\n✅ All API tests passed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to backend server.")
        print("Please make sure the backend is running at http://localhost:5000")
    except AssertionError as e:
        print(f"❌ Test failed: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    run_tests()
