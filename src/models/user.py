# models/user.py
from sqlalchemy import Column, String, Enum, DateTime, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from . import Base

class UserTypeEnum(str, enum.Enum):
    STUDENT = "student"
    TEACHER = "teacher"

class User(Base):
    __tablename__ = "users"
    
    # Primary Key
    user_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    
    # Basic Info
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    user_type = Column(Enum(UserTypeEnum), nullable=False, index=True)
    full_name = Column(String(255), nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    
    # Relationships (one-to-one with student or teacher)
    student = relationship(
        "Student",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )
    teacher = relationship(
        "Teacher",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )
    chat_history = relationship(
        "ChatHistory",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"<User(id={self.user_id}, email={self.email}, type={self.user_type})>"
    
    def to_dict(self):
        return {
            "user_id": str(self.user_id),
            "email": self.email,
            "user_type": self.user_type.value,
            "full_name": self.full_name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }