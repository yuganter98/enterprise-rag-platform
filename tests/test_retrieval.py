from app.services.rag.retriever import can_role_see, search_documents
from conftest import upload


def titles(role):
    return {d.metadata["title"] for d in search_documents("policy", role, top_k=10)}


def test_role_based_visibility(client, admin_headers):
    upload(client, admin_headers, "handbook.txt", b"Leave policy for all staff. " * 10)
    upload(client, admin_headers, "salaries.txt", b"Salary bands policy, HR only. " * 10, allowed_roles="hr")

    assert titles("employee") == {"handbook.txt"}
    assert titles("hr") == {"handbook.txt", "salaries.txt"}
    assert titles("admin") == {"handbook.txt", "salaries.txt"}


def test_empty_index_returns_nothing():
    assert search_documents("anything", "employee") == []


def test_legacy_chunks_use_uploader_role():
    assert can_role_see({"role": "employee"}, "employee")
    assert not can_role_see({"role": "admin"}, "employee")


def test_allowed_roles_take_precedence():
    assert can_role_see({"role": "admin", "allowed_roles": ["employee"]}, "employee")
    assert not can_role_see({"role": "employee", "allowed_roles": ["hr"]}, "employee")
