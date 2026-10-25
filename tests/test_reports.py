from app.models.employee import Employee


def add_employee(db, make_user, department="Eng"):
    user = make_user("ann@example.com")
    db.add(Employee(user_id=user.id, first_name="Ann", last_name="Lee", department=department, designation="Dev"))
    db.commit()


def test_report_404_without_employees(client, admin_headers):
    assert client.post("/api/v1/reports/employees", headers=admin_headers, json={"filters": {}}).status_code == 404


def test_report_downloads_xlsx(client, db, admin_headers, make_user):
    add_employee(db, make_user)
    r = client.post("/api/v1/reports/employees", headers=admin_headers, json={"filters": {"department": "Eng"}})
    assert r.status_code == 200
    assert r.content[:2] == b"PK"  # xlsx is a zip file
    assert "attachment" in r.headers["content-disposition"]


def test_report_filter_with_no_match(client, db, admin_headers, make_user):
    add_employee(db, make_user)
    r = client.post("/api/v1/reports/employees", headers=admin_headers, json={"filters": {"department": "Sales"}})
    assert r.status_code == 404


def test_hr_can_generate_report(client, db, hr_headers, make_user):
    add_employee(db, make_user)
    assert client.post("/api/v1/reports/employees", headers=hr_headers, json={"filters": {}}).status_code == 200


def test_employee_cannot_generate_report(client, employee_headers):
    assert client.post("/api/v1/reports/employees", headers=employee_headers, json={"filters": {}}).status_code == 403
