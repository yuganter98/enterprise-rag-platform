from app.db.session import SessionLocal
from app.models.user import User
from app.core.config import settings

print(f"DB URI: {settings.SQLALCHEMY_DATABASE_URI}")

db = SessionLocal()
user = db.query(User).first()
if user:
    print(f"User found: {user.email}")
else:
    print("No users found.")
db.close()
