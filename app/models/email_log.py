from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class EmailLog(Base):
    __tablename__ = "email_logs"

    id = Column(Integer, primary_key=True, index=True)
    recipient = Column(String, index=True, nullable=False)
    subject = Column(String, nullable=False)
    status = Column(String, default="sent")  # e.g., sent, failed
    triggered_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    sender = relationship("User", back_populates="email_logs")

    def __repr__(self):
        return f"<EmailLog(to={self.recipient}, status={self.status})>"
