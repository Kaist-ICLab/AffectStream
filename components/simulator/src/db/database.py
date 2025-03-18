from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from configurations import DBConfigurations

# Create a SQLAlchemy database engine
engine = create_engine(
    DBConfigurations.sql_alchemy_url, # DB connection URL
    pool_recycle=3600, # Recycle the connection after 1 hour to avoid timeout issues
    echo=False, # Disable SQL query logging for production use
)
# Create a SQLAlchemy session factory
SessionLocal = sessionmaker(autoflush=False, bind=engine)

def get_db() -> Session:
    """Get a database session instance.
    
    Returns:
        Session: A new database session.
    """
    return SessionLocal()

@contextmanager
def get_context_db():
    """Provide a database session using a context manager.
    
    Yields:
        Session: A database session that is automatically managed.
    
    Raises:
        Exception: If an error occurs, the session is rolled back before re-raising the exception.
    """
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
