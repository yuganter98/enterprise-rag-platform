"""
Seeds demo data: users for each role, employee records, an event, and the
sample company documents in sample_docs/ with role-based visibility.

Run after migrations and app.initial_data (the Docker entrypoint does those):
    python scripts/seed_demo.py
    docker compose exec api python scripts/seed_demo.py

Demo users share the password in DEMO_USER_PASSWORD (development falls back to
a default; production requires it). Safe to run more than once.
"""
import os
import shutil
import sys
import uuid
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.api.v1.endpoints.documents import UPLOAD_DIR  # noqa: E402
from app.core.config import settings  # noqa: E402
from app.core.security import get_password_hash  # noqa: E402
from app.db import base  # noqa: E402,F401 - registers all models
from app.db.session import SessionLocal  # noqa: E402
from app.models.document import Document  # noqa: E402
from app.models.employee import Employee  # noqa: E402
from app.models.event import Event  # noqa: E402
from app.models.role import Role  # noqa: E402
from app.models.user import User  # noqa: E402
from app.services.rag.service import ingest_document  # noqa: E402

SAMPLE_DOCS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sample_docs")
DEV_DEMO_PASSWORD = "demo-password-123"

# email, role, first name, last name, department, designation
DEMO_USERS = [
    ("employee@lumen.example", "employee", "Priya", "Shah", "Engineering", "Software Engineer II"),
    ("hr@lumen.example", "hr", "Marcus", "Bell", "People", "HR Business Partner"),
]
EXTRA_EMPLOYEES = [
    ("Lena", "Ortiz", "Engineering", "Senior Software Engineer"),
    ("Tom", "Nguyen", "Data", "Data Analyst"),
    ("Aisha", "Khan", "Engineering", "Engineering Manager"),
]
# filename -> roles allowed to retrieve it
DOCUMENTS = {
    "employee_handbook.txt": ["admin", "hr", "employee"],
    "it_security_policy.txt": ["admin", "hr", "employee"],
    "hr_compensation_guidelines.txt": ["admin", "hr"],
    "board_strategy_2027.txt": ["admin"],
}


def demo_password() -> str:
    password = os.environ.get("DEMO_USER_PASSWORD")
    if password:
        return password
    if settings.ENVIRONMENT == "production":
        sys.exit("DEMO_USER_PASSWORD must be set in production.")
    print(f"DEMO_USER_PASSWORD not set; using the development default '{DEV_DEMO_PASSWORD}'.")
    return DEV_DEMO_PASSWORD


def seed_users(db, password):
    for email, role_name, first, last, dept, title in DEMO_USERS:
        if db.query(User).filter(User.email == email).first():
            print(f"User exists: {email}")
            continue
        role = db.query(Role).filter(Role.name == role_name).one()
        user = User(email=email, hashed_password=get_password_hash(password), role_id=role.id, is_active=True)
        db.add(user)
        db.flush()
        db.add(Employee(user_id=user.id, first_name=first, last_name=last, department=dept, designation=title))
        print(f"Created {role_name}: {email}")

    # Employee records without logins, so reports have some rows
    for first, last, dept, title in EXTRA_EMPLOYEES:
        email = f"{first.lower()}.{last.lower()}@lumen.example"
        if db.query(User).filter(User.email == email).first():
            continue
        role = db.query(Role).filter(Role.name == "employee").one()
        user = User(email=email, hashed_password=get_password_hash(uuid.uuid4().hex), role_id=role.id, is_active=False)
        db.add(user)
        db.flush()
        db.add(Employee(user_id=user.id, first_name=first, last_name=last, department=dept, designation=title))
    db.commit()


def seed_event(db, admin):
    if db.query(Event).filter(Event.title == "Quarterly All-Hands").first():
        return
    db.add(Event(
        title="Quarterly All-Hands",
        description="Company update, product roadmap and Q&A with the leadership team.",
        date=datetime.utcnow().replace(hour=16, minute=0, second=0, microsecond=0) + timedelta(days=14),
        location="Main auditorium + video call",
        created_by_id=admin.id,
    ))
    db.commit()
    print("Created event: Quarterly All-Hands")


def seed_documents(db, admin):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    for filename, allowed_roles in DOCUMENTS.items():
        if db.query(Document).filter(Document.title == filename).first():
            print(f"Document exists: {filename}")
            continue
        destination = os.path.join(UPLOAD_DIR, f"{uuid.uuid4().hex}_{filename}")
        shutil.copyfile(os.path.join(SAMPLE_DOCS_DIR, filename), destination)
        chunks = ingest_document(destination, title=filename, user_id=admin.id, role="admin", allowed_roles=allowed_roles)
        db.add(Document(title=filename, file_path=destination, file_type="txt", uploaded_by=admin.id))
        db.commit()
        print(f"Ingested {filename} ({chunks} chunks) -> visible to {', '.join(allowed_roles)}")


def main():
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.email == settings.FIRST_SUPERUSER).first()
        if not admin:
            sys.exit("Admin user not found. Run `python -m app.initial_data` first.")
        seed_users(db, demo_password())
        seed_event(db, admin)
        seed_documents(db, admin)
        print("Demo data ready.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
