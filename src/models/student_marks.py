# models/student_mark.py
from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, Boolean, DECIMAL, text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime

from . import Base

class StudentMark(Base):
    __tablename__ = "student_marks"
    
    # Primary Key
    mark_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    
    # Foreign Keys
    student_id = Column(
        UUID(as_uuid=True),
        ForeignKey("students.student_id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    marksheet_id = Column(
        UUID(as_uuid=True),
        ForeignKey("marksheets.marksheet_id", ondelete="CASCADE"),
        nullable=False
    )
    subject_id = Column(
        UUID(as_uuid=True),
        ForeignKey("subjects.subject_id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Mark Details
    semester_number = Column(Integer, nullable=False, index=True)
    internal_marks = Column(DECIMAL(5, 2))
    external_marks = Column(DECIMAL(5, 2))
    total_marks = Column(DECIMAL(5, 2))
    grade = Column(String(5), index=True)
    result_date = Column(Date)
    has_backlog = Column(Boolean, default=False, nullable=False, index=True)
    
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
        UniqueConstraint(
            'student_id', 'subject_id', 'semester_number',
            name='unique_student_subject_semester'
        ),
    )
    
    # Relationships
    student = relationship("Student", back_populates="marks")
    marksheet = relationship("Marksheet", back_populates="marks")
    subject = relationship("Subject", back_populates="marks")
    
    def __repr__(self):
        return f"<StudentMark(student={self.student_id}, subject={self.subject_id}, marks={self.total_marks})>"
    
    def to_dict(self):
        return {
            "mark_id": str(self.mark_id),
            "student_id": str(self.student_id),
            "marksheet_id": str(self.marksheet_id),
            "subject_id": str(self.subject_id),
            "semester_number": self.semester_number,
            "internal_marks": float(self.internal_marks) if self.internal_marks else None,
            "external_marks": float(self.external_marks) if self.external_marks else None,
            "total_marks": float(self.total_marks) if self.total_marks else None,
            "grade": self.grade,
            "result_date": self.result_date.isoformat() if self.result_date else None,
            "has_backlog": self.has_backlog,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }