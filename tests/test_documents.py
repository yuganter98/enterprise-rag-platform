import os

from app.api.v1.endpoints.documents import UPLOAD_DIR, sanitize_filename
from conftest import upload

TEXT = b"Vacation policy: employees get 20 days of paid leave per year. " * 10


def test_admin_upload_defaults_to_all_roles(client, admin_headers):
    r = upload(client, admin_headers, "handbook.txt", TEXT)
    assert r.status_code == 200, r.text
    assert r.json()["allowed_roles"] == ["admin", "hr", "employee"]
    assert r.json()["chunks"] >= 1


def test_upload_with_restricted_roles(client, admin_headers):
    r = upload(client, admin_headers, "salaries.txt", TEXT, allowed_roles="hr")
    assert r.json()["allowed_roles"] == ["hr"]


def test_upload_unknown_role_rejected(client, admin_headers):
    assert upload(client, admin_headers, "a.txt", TEXT, allowed_roles="ceo").status_code == 400


def test_employee_cannot_upload(client, employee_headers):
    assert upload(client, employee_headers, "a.txt", TEXT).status_code == 403


def test_hr_cannot_upload(client, hr_headers):
    assert upload(client, hr_headers, "a.txt", TEXT).status_code == 403


def test_disallowed_extension(client, admin_headers):
    assert upload(client, admin_headers, "evil.exe", b"MZ").status_code == 400


def test_oversized_upload(client, admin_headers):
    big = b"a" * (1024 * 1024 + 1)  # MAX_UPLOAD_SIZE_MB=1 in tests
    assert upload(client, admin_headers, "big.txt", big).status_code == 413
    assert os.listdir(UPLOAD_DIR) == []


def test_path_traversal_stays_in_upload_dir(client, admin_headers):
    r = upload(client, admin_headers, "../../../escape.txt", TEXT)
    assert r.status_code == 200
    saved = os.listdir(UPLOAD_DIR)
    assert len(saved) == 1 and saved[0].endswith("_escape.txt")


def test_same_name_uploads_do_not_overwrite(client, admin_headers):
    upload(client, admin_headers, "same.txt", TEXT)
    upload(client, admin_headers, "same.txt", TEXT)
    assert len(os.listdir(UPLOAD_DIR)) == 2


def test_failed_ingestion_removes_file(client, admin_headers):
    r = upload(client, admin_headers, "broken.pdf", b"not really a pdf")
    assert r.status_code == 422
    assert os.listdir(UPLOAD_DIR) == []


def test_sanitize_filename():
    assert sanitize_filename("..\\..\\win.txt") == "win.txt"
    assert sanitize_filename("a/b/c.pdf") == "c.pdf"
    assert sanitize_filename("we<ird>|name.txt") == "we_ird__name.txt"
    assert sanitize_filename("..") == "upload"
