from types import SimpleNamespace

import app.services.rag.chat as chat_service
from conftest import upload


class FakeLLM:
    def __init__(self):
        self.prompts = []

    def invoke(self, prompt):
        self.prompts.append(prompt)
        return SimpleNamespace(content="You get 20 days of leave.")


def test_chat_without_documents(client, employee_headers):
    r = client.post("/api/v1/chat/", headers=employee_headers, json={"query": "leave?"})
    assert r.status_code == 200
    assert "couldn't find any relevant documents" in r.json()["response"]


def test_chat_uses_retrieved_context(client, admin_headers, employee_headers, monkeypatch):
    llm = FakeLLM()
    monkeypatch.setattr(chat_service, "get_llm", lambda: llm)
    upload(client, admin_headers, "handbook.txt", b"Employees get 20 days of paid leave. " * 10)

    r = client.post("/api/v1/chat/", headers=employee_headers, json={"query": "How much leave?"})
    assert r.json()["response"] == "You get 20 days of leave."
    assert "20 days of paid leave" in llm.prompts[0]


def test_chat_does_not_leak_restricted_context(client, admin_headers, employee_headers, monkeypatch):
    llm = FakeLLM()
    monkeypatch.setattr(chat_service, "get_llm", lambda: llm)
    upload(client, admin_headers, "public.txt", b"Office opens at 9am. " * 10)
    upload(client, admin_headers, "secret.txt", b"CEO salary is confidential. " * 10, allowed_roles="admin")

    client.post("/api/v1/chat/", headers=employee_headers, json={"query": "salary"})
    assert "confidential" not in llm.prompts[0]
