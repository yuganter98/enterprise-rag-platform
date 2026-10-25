from app.core.security import create_access_token
from conftest import ADMIN_EMAIL, ADMIN_PASSWORD, USER_PASSWORD


def test_login_returns_token(client):
    r = client.post("/api/v1/login/access-token", data={"username": ADMIN_EMAIL, "password": ADMIN_PASSWORD})
    assert r.status_code == 200
    assert r.json()["token_type"] == "bearer"


def test_login_wrong_password(client):
    r = client.post("/api/v1/login/access-token", data={"username": ADMIN_EMAIL, "password": "wrong"})
    assert r.status_code == 400


def test_login_inactive_user(client, make_user):
    make_user("gone@example.com", is_active=False)
    r = client.post("/api/v1/login/access-token", data={"username": "gone@example.com", "password": USER_PASSWORD})
    assert r.status_code == 400


def test_missing_token_is_401(client):
    assert client.get("/api/v1/users/me").status_code == 401


def test_garbage_token_is_401(client):
    r = client.get("/api/v1/users/me", headers={"Authorization": "Bearer not-a-jwt"})
    assert r.status_code == 401
    assert r.headers["www-authenticate"] == "Bearer"


def test_token_for_deleted_user_is_401(client):
    token = create_access_token(99999)
    r = client.get("/api/v1/users/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 401


def test_token_for_deactivated_user_is_403(client, db, make_user):
    user = make_user("later-disabled@example.com")
    token = create_access_token(user.id)
    user.is_active = False
    db.commit()
    r = client.get("/api/v1/users/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 403


def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}
