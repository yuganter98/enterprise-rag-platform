import app.db.base # Load all models
from app.db.session import SessionLocal
from app.models.user import User
from sqlalchemy import text

print("Testing DB Connection...")
try:
    db = SessionLocal()
    # Try a raw query
    db.execute(text("SELECT 1"))
    print("   Connection: OK")
    
    # Try ORM query
    user = db.query(User).first()
    if user:
        print(f"   ORM Query: OK (Found user {user.email})")
    else:
        print("   ORM Query: OK (No users found)")
    db.close()
    print("Test Passed.")
except Exception:
    import traceback
    traceback.print_exc()
