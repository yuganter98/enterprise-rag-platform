from sqlalchemy import text
from app.db.session import engine
from app.core.config import settings
from app.core.security import get_password_hash

def init_raw() -> None:
    print(f"Seeding DB: {settings.SQLALCHEMY_DATABASE_URI}")
    
    with engine.connect() as conn:
        # 1. Seed Roles
        roles = ["admin", "hr", "employee"]
        role_map = {}
        
        for role_name in roles:
            # Check exist (Parametrized for safety)
            result = conn.execute(text("SELECT id FROM roles WHERE name = :name"), {"name": role_name}).fetchone()
            
            if result:
                role_map[role_name] = result[0]
                print(f"Role exists: {role_name}")
            else:
                # Insert
                # PostgreSQL returning ID
                if "postgresql" in str(settings.SQLALCHEMY_DATABASE_URI):
                    stmt = text("INSERT INTO roles (name) VALUES (:name) RETURNING id")
                    res = conn.execute(stmt, {"name": role_name}).fetchone()
                    role_id = res[0]
                else:
                    # SQLite / Others
                    conn.execute(text("INSERT INTO roles (name) VALUES (:name)"), {"name": role_name})
                    # Get ID
                    res = conn.execute(text("SELECT id FROM roles WHERE name = :name"), {"name": role_name}).fetchone()
                    role_id = res[0]
                
                role_map[role_name] = role_id
                print(f"Created role: {role_name}")

        # 2. Seed Superuser
        email = settings.FIRST_SUPERUSER
        password = settings.FIRST_SUPERUSER_PASSWORD
        
        user_res = conn.execute(text("SELECT id FROM users WHERE email = :email"), {"email": email}).fetchone()
        
        if user_res:
            print(f"Superuser exists: {email}")
        else:
            admin_role_id = role_map.get("admin")
            hashed_pw = get_password_hash(password)
            
            conn.execute(
                text("INSERT INTO users (email, hashed_password, is_active, role_id) VALUES (:email, :password, :active, :role_id)"),
                {
                    "email": email,
                    "password": hashed_pw,
                    "active": True,
                    "role_id": admin_role_id
                }
            )
            print(f"Created superuser: {email}")

        conn.commit()
        print("Database initialized successfully.")

if __name__ == "__main__":
    init_raw()
