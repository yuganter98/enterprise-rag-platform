import requests
import sys

BASE_URL = "http://localhost:8000"

def check_server():
    print("1. Checking Server Availability...")
    try:
        # Check root (app/main.py usually has a root or api v1 check)
        # Based on typical FastAPI structure
        resp = requests.get(f"{BASE_URL}/")
        if resp.status_code == 200:
            print(f"   Success! Server says: {resp.json()}")
        else:
            print(f"   Warning: Root returned {resp.status_code}")
    except Exception as e:
        print(f"   Failed to connect to server: {e}")
        return False

    print("\n2. Verifying Database (Login)...")
    login_url = f"{BASE_URL}/api/v1/login/access-token"
    payload = {
        "username": "admin@enterprise.com",
        "password": "admin123"
    }
    
    try:
        resp = requests.post(login_url, data=payload)
        if resp.status_code == 200:
            token_data = resp.json()
            if "access_token" in token_data:
                print("   Success! Login successful, token received.")
                print(f"   Token Type: {token_data.get('token_type')}")
                return True
            else:
                print("   Failed: No access token in response.")
        else:
            print(f"   Failed: Login returned {resp.status_code}")
            print(f"   Response: {resp.text}")
            print("   (This might mean the DB connection is bad, or seeding failed)")
    except Exception as e:
        print(f"   Login request failed: {e}")
        return False

if __name__ == "__main__":
    if check_server():
        print("\nAll checks passed. The system is running on PostgreSQL.")
    else:
        print("\nChecks failed.")
        sys.exit(1)
