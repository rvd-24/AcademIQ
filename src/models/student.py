# models/student.py
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime

from . import Base

class Student(Base):
    __tablename__ = "students"
    
    # Primary Key
    student_id = Column(
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
    
    # Student Info
    registration_number = Column(String(50), unique=True, nullable=False, index=True)
    department = Column(String(100), index=True)
    batch_year = Column(Integer, index=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    
    # Relationships
    user = relationship("User", back_populates="student")
    marksheets = relationship(
        "Marksheet",
        back_populates="student",
        cascade="all, delete-orphan"
    )
    marks = relationship(
        "StudentMark",
        back_populates="student",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"<Student(id={self.student_id}, reg_no={self.registration_number})>"
    
    def to_dict(self):
        return {
            "student_id": str(self.student_id),
            "user_id": str(self.user_id),
            "registration_number": self.registration_number,
            "department": self.department,
            "batch_year": self.batch_year,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }