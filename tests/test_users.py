def test_roles_endpoint_lists_seeded_roles(client, admin_headers):
    names = [r["name"] for r in client.get("/api/v1/users/roles", headers=admin_headers).json()]
    assert names == ["admin", "hr", "employee"]


def test_create_user_defaults_to_employee(client, admin_headers):
    r = client.post("/api/v1/users/", headers=admin_headers, json={"email": "new@example.com", "password": "long-enough"})
    assert r.status_code == 200
    assert r.json()["role"]["name"] == "employee"


def test_create_user_with_explicit_role(client, admin_headers):
    roles = client.get("/api/v1/users/roles", headers=admin_headers).json()
    hr_id = next(r["id"] for r in roles if r["name"] == "hr")
    r = client.post(
        "/api/v1/users/",
        headers=admin_headers,
        json={"email": "hr2@example.com", "password": "long-enough", "role_id": hr_id},
    )
    assert r.json()["role"]["name"] == "hr"


def test_create_user_invalid_role(client, admin_headers):
    r = client.post(
        "/api/v1/users/",
        headers=admin_headers,
        json={"email": "x@example.com", "password": "long-enough", "role_id": 999},
    )
    assert r.status_code == 400


def test_create_user_short_password(client, admin_headers):
    r = client.post("/api/v1/users/", headers=admin_headers, json={"email": "x@example.com", "password": "short"})
    assert r.status_code == 422


def test_create_user_duplicate_email(client, admin_headers):
    body = {"email": "dup@example.com", "password": "long-enough"}
    assert client.post("/api/v1/users/", headers=admin_headers, json=body).status_code == 200
    assert client.post("/api/v1/users/", headers=admin_headers, json=body).status_code == 400


def test_employee_cannot_create_users(client, employee_headers):
    r = client.post("/api/v1/users/", headers=employee_headers, json={"email": "x@example.com", "password": "long-enough"})
    assert r.status_code == 403


def test_employee_only_sees_self(client, employee_headers):
    users = client.get("/api/v1/users/", headers=employee_headers).json()
    assert [u["email"] for u in users] == ["employee@example.com"]
