# database.py
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import os

# Import Base from models
from models import Base

# Create database URL
url = URL.create(
    drivername="postgresql+psycopg2",
    username=os.environ['DB_USER'],
    password=os.environ['DB_PASS'],
    host=os.environ['DB_HOST'],
    port=5432,
    database='dev-academiq'
)

# Create engine
engine = create_engine(
    url,
    pool_size=10,
    max_overflow=20,
    pool_recycle=3600,
    pool_pre_ping=True,
    echo=True,  # Set to False in production
    connect_args={
        "sslmode": "require",
        "connect_timeout": 10,
        "options": "-c timezone=utc"
    }
)

# Create Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency for FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Context manager
@contextmanager
def get_db_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

# Initialize database (create all tables)
def init_db():
    """Create all tables defined in ORM models"""
    Base.metadata.create_all(bind=engine)
    print("✅ All tables created successfully!")

def drop_all_tables():
    """Drop all tables (use with caution!)"""
    Base.metadata.drop_all(bind=engine)
    print("⚠️ All tables dropped!")

# Test connection
def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute("SELECT 1")
            print("Database connection successful!")
            return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False