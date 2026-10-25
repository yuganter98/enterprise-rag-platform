import pytest
from pydantic import ValidationError

from app.core.config import DEV_SUPERUSER_PASSWORD, Settings

STRONG_KEY = "k" * 40


def make(**overrides):
    base = {
        "ENVIRONMENT": "production",
        "SECRET_KEY": STRONG_KEY,
        "FIRST_SUPERUSER_PASSWORD": "Str0ng-admin-pass",
        "SQLALCHEMY_DATABASE_URI": "sqlite:///x.db",
    }
    return Settings(_env_file=None, **{**base, **overrides})


def test_production_accepts_secure_settings():
    assert make().SECRET_KEY == STRONG_KEY


@pytest.mark.parametrize("overrides, message", [
    ({"SECRET_KEY": ""}, "SECRET_KEY is not set"),
    ({"SECRET_KEY": "short"}, "at least 32"),
    ({"FIRST_SUPERUSER_PASSWORD": DEV_SUPERUSER_PASSWORD}, "FIRST_SUPERUSER_PASSWORD"),
    ({"SQLALCHEMY_DATABASE_URI": "", "POSTGRES_PASSWORD": "password"}, "POSTGRES_PASSWORD"),
])
def test_production_rejects_insecure_settings(overrides, message):
    with pytest.raises(ValidationError, match=message):
        make(**overrides)


def test_development_generates_key_and_warns():
    with pytest.warns(UserWarning, match="development only"):
        s = make(ENVIRONMENT="development", SECRET_KEY="")
    assert len(s.SECRET_KEY) >= 32


@pytest.mark.parametrize("raw", [
    "http://localhost:5173",
    "http://localhost:5173, https://app.example.com",
    '["http://localhost:5173", "https://app.example.com"]',
])
def test_cors_origins_from_env(monkeypatch, raw):
    monkeypatch.setenv("BACKEND_CORS_ORIGINS", raw)
    origins = [str(o).rstrip("/") for o in make().BACKEND_CORS_ORIGINS]
    assert origins[0] == "http://localhost:5173"
    assert len(origins) == raw.count("http")


def test_cors_origins_empty_env(monkeypatch):
    monkeypatch.setenv("BACKEND_CORS_ORIGINS", "")
    assert make().BACKEND_CORS_ORIGINS == []
