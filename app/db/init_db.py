from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import get_password_hash
from app.models.role import Role
from app.models.user import User

def init_db(db: Session) -> None:
    # 1. Create Roles
    roles = ["admin", "hr", "employee"]
    for role_name in roles:
        role = db.query(Role).filter(Role.name == role_name).first()
        if not role:
            role = Role(name=role_name)
            db.add(role)
            db.commit()
            print(f"Created role: {role_name}")
        else:
            print(f"Role already exists: {role_name}")

    # 2. Create Superuser
    user = db.query(User).filter(User.email == settings.FIRST_SUPERUSER).first()
    if not user:
        # Get admin role
        admin_role = db.query(Role).filter(Role.name == "admin").first()
        
        user = User(
            email=settings.FIRST_SUPERUSER,
            hashed_password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
            role_id=admin_role.id,
            is_active=True,
        )
        db.add(user)
        db.commit()
        print(f"Created superuser: {settings.FIRST_SUPERUSER}")
    else:
        print(f"Superuser already exists: {settings.FIRST_SUPERUSER}")
