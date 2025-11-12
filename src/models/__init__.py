# models/__init__.py
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Import all models here for easy access
from .user import User
from .student import Student
from .teacher import Teacher
from .subject import Subject
from .marksheet import Marksheet
from .student_mark import StudentMark
from .chat_history import ChatHistory

__all__ = [
    "Base",
    "User",
    "Student",
    "Teacher",
    "Subject",
    "Marksheet",
    "StudentMark",
    "ChatHistory"
]