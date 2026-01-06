from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    department = Column(String, index=True)
    designation = Column(String)

    user = relationship("User", back_populates="employee")

    def __repr__(self):
        return f"<Employee(name={self.first_name} {self.last_name})>"
