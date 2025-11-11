"""
SQLAlchemy models for all database tables.
These models match the schema already created in pgAdmin.
"""
from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import (
    Column, Integer, String, Text, SmallInteger, Date, Boolean,
    ForeignKey, UniqueConstraint, Index, JSON as SQLJSON, DateTime
)
from sqlalchemy.dialects.postgresql import UUID as PGUUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.config.database import Base
