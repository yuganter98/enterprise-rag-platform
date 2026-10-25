from app.models.email_log import EmailLog


def test_email_all_expands_to_active_users(client, db, admin_headers, make_user):
    make_user("a@example.com")
    make_user("inactive@example.com", is_active=False)
    r = client.post("/api/v1/email/send", headers=admin_headers, json={"to_email": "all", "subject": "Hi", "body": "x"})
    assert r.status_code == 200
    recipients = {log.recipient for log in db.query(EmailLog).filter(EmailLog.subject == "Hi")}
    assert recipients == {"admin@example.com", "a@example.com"}


def test_email_comma_list(client, db, admin_headers):
    client.post(
        "/api/v1/email/send",
        headers=admin_headers,
        json={"to_email": "x@example.com, y@example.com", "subject": "List", "body": "x"},
    )
    assert db.query(EmailLog).filter(EmailLog.subject == "List").count() == 2


def test_employee_cannot_mass_email(client, employee_headers):
    r = client.post("/api/v1/email/send", headers=employee_headers, json={"to_email": "all", "subject": "x", "body": "x"})
    assert r.status_code == 403


def test_employee_can_email_one_person(client, employee_headers):
    r = client.post(
        "/api/v1/email/send",
        headers=employee_headers,
        json={"to_email": "boss@example.com", "subject": "x", "body": "x"},
    )
    assert r.status_code == 200


def test_event_creation_notifies_everyone(client, db, admin_headers, make_user):
    make_user("a@example.com")
    r = client.post("/api/v1/events/", headers=admin_headers, json={"title": "Offsite", "date": "2026-11-01T10:00:00"})
    assert r.status_code == 200
    # TestClient runs background tasks before returning
    assert db.query(EmailLog).filter(EmailLog.subject == "New Event: Offsite").count() == 2


def test_hr_can_create_event(client, hr_headers):
    r = client.post("/api/v1/events/", headers=hr_headers, json={"title": "Party", "date": "2026-12-20T18:00:00"})
    assert r.status_code == 200


def test_employee_cannot_create_event(client, employee_headers):
    r = client.post("/api/v1/events/", headers=employee_headers, json={"title": "x", "date": "2026-11-01T10:00:00"})
    assert r.status_code == 403


def test_events_listed_newest_first(client, admin_headers, employee_headers):
    client.post("/api/v1/events/", headers=admin_headers, json={"title": "Early", "date": "2026-01-01T10:00:00"})
    client.post("/api/v1/events/", headers=admin_headers, json={"title": "Late", "date": "2026-12-01T10:00:00"})
    titles = [e["title"] for e in client.get("/api/v1/events/", headers=employee_headers).json()]
    assert titles == ["Late", "Early"]
