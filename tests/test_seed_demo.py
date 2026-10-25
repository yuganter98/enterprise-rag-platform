import importlib.util
import os

from app.models.document import Document
from app.models.employee import Employee
from app.models.user import User
from app.services.rag.retriever import search_documents

SCRIPT = os.path.join(os.path.dirname(os.path.dirname(__file__)), "scripts", "seed_demo.py")


def load_seed_module():
    spec = importlib.util.spec_from_file_location("seed_demo", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_seed_demo_is_idempotent_and_respects_roles(db):
    seed = load_seed_module()
    seed.main()
    seed.main()  # second run must not duplicate anything

    assert db.query(User).filter(User.email == "employee@lumen.example").count() == 1
    assert db.query(Document).count() == len(seed.DOCUMENTS)
    assert db.query(Employee).count() == len(seed.DEMO_USERS) + len(seed.EXTRA_EMPLOYEES)

    def titles(role):
        return {d.metadata["title"] for d in search_documents("policy salary strategy", role, top_k=50)}

    assert titles("employee") == {"employee_handbook.txt", "it_security_policy.txt"}
    assert titles("hr") == {"employee_handbook.txt", "it_security_policy.txt", "hr_compensation_guidelines.txt"}
    assert "board_strategy_2027.txt" in titles("admin")
