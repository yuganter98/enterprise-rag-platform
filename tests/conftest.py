"""
Shared test fixtures.

Tests run against a throwaway SQLite database and data directory, with a
deterministic fake embedding model, so no GPU, model download, LLM or
Postgres is needed.
"""
import os
import shutil
import tempfile

# Settings are read at import time, so configure the environment first.
_TEST_DIR = tempfile.mkdtemp(prefix="rag-tests-")
os.environ.update({
    "ENVIRONMENT": "development",
    "SECRET_KEY": "test-secret-key-that-is-long-enough-1234567890",
    "SQLALCHEMY_DATABASE_URI": f"sqlite:///{os.path.join(_TEST_DIR, 'test.db')}",
    "DATA_DIR": os.path.join(_TEST_DIR, "data"),
    "FIRST_SUPERUSER": "admin@example.com",
    "FIRST_SUPERUSER_PASSWORD": "admin-test-password",
    "MAX_UPLOAD_SIZE_MB": "1",
    "SMTP_HOST": "",
})

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from langchain_core.embeddings import DeterministicFakeEmbedding  # noqa: E402

import app.services.rag.vector_store as vector_store  # noqa: E402
from app.core.config import settings  # noqa: E402
from app.db.base import Base  # noqa: E402
from app.db.init_db import init_db  # noqa: E402
from app.db.session import SessionLocal, engine  # noqa: E402
from app.main import app  # noqa: E402
from app.models.role import Role  # noqa: E402
from app.models.user import User  # noqa: E402
from app.core.security import get_password_hash  # noqa: E402

ADMIN_EMAIL = settings.FIRST_SUPERUSER
ADMIN_PASSWORD = settings.FIRST_SUPERUSER_PASSWORD
USER_PASSWORD = "user-test-password"


@pytest.fixture(autouse=True)
def fresh_state(monkeypatch):
    """Fresh database, data directory and fake embeddings for every test."""
    monkeypatch.setattr(vector_store, "get_embeddings", lambda: DeterministicFakeEmbedding(size=64))

    shutil.rmtree(settings.DATA_DIR, ignore_errors=True)
    os.makedirs(os.path.join(settings.DATA_DIR, "uploads"), exist_ok=True)

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    init_db(db)
    db.close()
    yield


@pytest.fixture
def db():
    session = SessionLocal()
    yield session
    session.close()


@pytest.fixture
def client():
    return TestClient(app)


def login(client, email, password):
    r = client.post("/api/v1/login/access-token", data={"username": email, "password": password})
    assert r.status_code == 200, r.text
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


@pytest.fixture
def admin_headers(client):
    return login(client, ADMIN_EMAIL, ADMIN_PASSWORD)


@pytest.fixture
def make_user(db):
    """Creates a user with the given role and returns it."""
    def _make(email, role="employee", is_active=True):
        role_obj = db.query(Role).filter(Role.name == role).one()
        user = User(
            email=email,
            hashed_password=get_password_hash(USER_PASSWORD),
            role_id=role_obj.id,
            is_active=is_active,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    return _make


@pytest.fixture
def employee_headers(client, make_user):
    make_user("employee@example.com", "employee")
    return login(client, "employee@example.com", USER_PASSWORD)


@pytest.fixture
def hr_headers(client, make_user):
    make_user("hr@example.com", "hr")
    return login(client, "hr@example.com", USER_PASSWORD)


def upload(client, headers, filename, content, allowed_roles=None):
    data = {"allowed_roles": allowed_roles} if allowed_roles is not None else {}
    return client.post(
        "/api/v1/documents/upload",
        headers=headers,
        files={"file": (filename, content)},
        data=data,
    )
