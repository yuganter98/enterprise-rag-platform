# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.role import Role  # noqa
from app.models.user import User  # noqa
from app.models.employee import Employee  # noqa
from app.models.document import Document
from app.models.email_log import EmailLog
from app.models.event import Event  # noqa
