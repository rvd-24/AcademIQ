# models/subject.py
from sqlalchemy import Column, String, DateTime, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime

from . import Base

class Subject(Base):
    __tablename__ = "subjects"
    
    # Primary Key
    subject_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    
    # Subject Info
    subject_code = Column(String(50), unique=True, nullable=False, index=True)
    subject_name = Column(String(255), nullable=False, index=True)
    department = Column(String(100), index=True)
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    marks = relationship(
        "StudentMark",
        back_populates="subject",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"<Subject(code={self.subject_code}, name={self.subject_name})>"
    
    def to_dict(self):
        return {
            "subject_id": str(self.subject_id),
            "subject_code": self.subject_code,
            "subject_name": self.subject_name,
            "department": self.department,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }