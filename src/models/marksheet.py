# models/marksheet.py
from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, Enum, text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from . import Base

class ProcessingStatusEnum(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class Marksheet(Base):
    __tablename__ = "marksheets"
    
    # Primary Key
    marksheet_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    
    # Foreign Key
    student_id = Column(
        UUID(as_uuid=True),
        ForeignKey("students.student_id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Marksheet Info
    semester_number = Column(Integer, nullable=False, index=True)
    result_date = Column(Date)
    blob_storage_url = Column(String(500), nullable=False)
    upload_date = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    processing_status = Column(
        Enum(ProcessingStatusEnum),
        default=ProcessingStatusEnum.PENDING,
        nullable=False,
        index=True
    )
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    
    # Unique Constraint
    __table_args__ = (
        UniqueConstraint('student_id', 'semester_number', name='unique_student_semester'),
    )
    
    # Relationships
    student = relationship("Student", back_populates="marksheets")
    marks = relationship(
        "StudentMark",
        back_populates="marksheet",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"<Marksheet(id={self.marksheet_id}, student={self.student_id}, sem={self.semester_number})>"
    
    def to_dict(self):
        return {
            "marksheet_id": str(self.marksheet_id),
            "student_id": str(self.student_id),
            "semester_number": self.semester_number,
            "result_date": self.result_date.isoformat() if self.result_date else None,
            "blob_storage_url": self.blob_storage_url,
            "upload_date": self.upload_date.isoformat() if self.upload_date else None,
            "processing_status": self.processing_status.value,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }