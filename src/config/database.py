"""
Database configuration and connection setup for PostgreSQL using SQLAlchemy async engine.
"""
import os
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import declarative_base

# Database connection URL
# Format: postgresql+asyncpg://user:password@host:port/database

url = URL.create(
    drivername="postgresql+asyncpg",
    username="db_admin",
    password=os.environ.get("DB_PASSWORD"),
    host=os.environ.get("DB_HOST"),
    port=5432,
    database='dev-academiq'
)

# Create async engine
engine = create_async_engine(
    url,
    future=True,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Base class for all models
Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency function for FastAPI to get database session.
    Usage in FastAPI routes:
        @app.get("/example")
        async def example(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """
    Initialize database (create tables if they don't exist).
    Note: Since tables are already created in pgAdmin, this is optional.
    """
    async with engine.begin() as conn:
        # Uncomment if you want SQLAlchemy to create tables
        # await conn.run_sync(Base.metadata.create_all)
        pass


async def close_db():
    """Close database connections."""
    await engine.dispose()

