from sqlalchemy.engine import create_engine, URL
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager
import os

url = URL.create(
    drivername="postgresql+psycopg2",
    username = os.environ['DB_USER'],
    password = os.environ['DB_PASS'],
    host = os.environ['DB_HOST'],
    port = 5432,
    database = os.environ['DB_DATABASE']
)
engine = create_engine(
    url,
    pool_size = 10,
    max_overflow = 20,
    pool_timeout = 30,
    pool_recycle = 3600,
    pool_pre_ping = True)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    """
    FastAPI dependency to get database session.
    Usage:
        @app.get("/endpoint")
        async def endpoint(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Context manager for manual session handling
@contextmanager
def get_db_session():
    """
    Context manager for manual database operations.
    Usage:
        with get_db_session() as session:
            result = session.execute(query)
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()