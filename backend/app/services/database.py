"""
Enhanced database session management with connection pooling
"""
from sqlmodel import create_engine, Session
from ..config import NEON_DATABASE_URL
from sqlalchemy.pool import QueuePool
from contextlib import contextmanager

# Create the database engine with connection pooling
engine = create_engine(
    NEON_DATABASE_URL,
    echo=False,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=300
)

@contextmanager
def get_db_session():
    """Get a database session with proper cleanup"""
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

def get_db_session_generator():
    """Generator for dependency injection"""
    with get_db_session() as session:
        yield session