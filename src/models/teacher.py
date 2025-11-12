# models/teacher.py
from sqlalchemy import Column, String, ForeignKey, DateTime, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime

from . import Base

class Teacher(Base):
    __tablename__ = "teachers"
    
    # Primary Key
    teacher_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    
    # Foreign Key
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )
    
    # Teacher Info
    employee_id = Column(String(50), unique=True, index=True)
    department = Column(String(100), index=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    
    # Relationships
    user = relationship("User", back_populates="teacher")
    
    def __repr__(self):
        return f"<Teacher(id={self.teacher_id}, emp_id={self.employee_id})>"
    
    def to_dict(self):
        return {
            "teacher_id": str(self.teacher_id),
            "user_id": str(self.user_id),
            "employee_id": self.employee_id,
            "department": self.department,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }