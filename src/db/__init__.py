"""
Database module exports.
Import all models, views, and utilities from here.
"""
from config.database import (
    Base,
    engine,
    AsyncSessionLocal,
    get_db,
    init_db,
    close_db,
    DATABASE_URL,
)

from models import (
    User,
    Student,
    Teacher,
    Subject,
    Marksheet,
    StudentMark,
    ChatHistory,
)

__all__ = [
    # Database configuration
    "Base",
    "engine",
    "AsyncSessionLocal",
    "get_db",
    "init_db",
    "close_db",
    "DATABASE_URL",
    # Models
    "User",
    "Student",
    "Teacher",
    "Subject",
    "Marksheet",
    "StudentMark",
    "ChatHistory",
]

