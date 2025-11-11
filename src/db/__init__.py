"""
Database module exports.
Import all models, views, and utilities from here.
"""
from src.config.database import (
    Base,
    engine,
    AsyncSessionLocal,
    get_db,
    init_db,
    close_db,
    DATABASE_URL,
)

from src.db.models import (
    Branch,
    Subject,
    Student,
    StudentAlias,
    IngestionLog,
    ExamResult,
    AuditLog,
)

from src.db.views import (
    StudentTotal,
    StudentAnalyticsRaw,
    StudentChat,
    TeacherResult,
)

from src.db.session import (
    DatabaseSession,
    get_db_session,
)

from src.db.functions import (
    get_student_summary,
    refresh_materialized_view,
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
    "Branch",
    "Subject",
    "Student",
    "StudentAlias",
    "IngestionLog",
    "ExamResult",
    "AuditLog",
    # Views
    "StudentTotal",
    "StudentAnalyticsRaw",
    "StudentChat",
    "TeacherResult",
    # Session management
    "DatabaseSession",
    "get_db_session",
    # Functions
    "get_student_summary",
    "refresh_materialized_view",
]

