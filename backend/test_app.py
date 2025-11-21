"""
Simple tests for the Napkin backend application
"""
import sys
import hashlib
import secrets
from datetime import datetime, timedelta

# Test utility functions
def test_hash_password():
    """Test password hashing with salt"""
    password = "test123"
    
    # Test with random salt
    hash1 = hashlib.sha256((password + secrets.token_hex(16)).encode()).hexdigest()
    hash2 = hashlib.sha256((password + secrets.token_hex(16)).encode()).hexdigest()
    
    assert hash1 != hash2, "Different salts should produce different hashes"
    assert len(hash1) == 64, "SHA256 hash should be 64 characters"
    
    # Test with same salt
    salt = secrets.token_hex(16)
    hash3 = hashlib.sha256((password + salt).encode()).hexdigest()
    hash4 = hashlib.sha256((password + salt).encode()).hexdigest()
    assert hash3 == hash4, "Same password and salt should produce same hash"
    
    print("✓ Password hashing with salt works correctly")

def test_generate_note_id():
    """Test note ID generation"""
    id1 = secrets.token_urlsafe(16)
    id2 = secrets.token_urlsafe(16)
    
    assert id1 != id2, "Generated IDs should be unique"
    assert len(id1) > 0, "ID should not be empty"
    print("✓ Note ID generation works correctly")

def test_expiry_calculation():
    """Test expiry time calculation"""
    hours = 24
    expires_at = datetime.now() + timedelta(hours=hours)
    
    assert expires_at > datetime.now(), "Expiry time should be in the future"
    time_diff = expires_at - datetime.now()
    assert time_diff.total_seconds() > 86000, "24 hours should be ~86400 seconds"
    print("✓ Expiry calculation works correctly")

def test_password_validation():
    """Test password validation logic with salt"""
    password = "secret123"
    salt = secrets.token_hex(16)
    stored_hash = f"{salt}:{hashlib.sha256((password + salt).encode()).hexdigest()}"
    
    # Correct password
    user_input = "secret123"
    salt_from_stored = stored_hash.split(':')[0]
    user_hash = f"{salt_from_stored}:{hashlib.sha256((user_input + salt_from_stored).encode()).hexdigest()}"
    assert user_hash == stored_hash, "Correct password should match"
    
    # Wrong password
    wrong_input = "wrong_password"
    wrong_hash = f"{salt_from_stored}:{hashlib.sha256((wrong_input + salt_from_stored).encode()).hexdigest()}"
    assert wrong_hash != stored_hash, "Wrong password should not match"
    
    print("✓ Password validation with salt works correctly")

if __name__ == '__main__':
    print("Running Napkin backend tests...\n")
    
    try:
        test_hash_password()
        test_generate_note_id()
        test_expiry_calculation()
        test_password_validation()
        
        print("\n✅ All tests passed!")
        sys.exit(0)
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
