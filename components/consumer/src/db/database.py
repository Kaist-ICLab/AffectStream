from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from configurations import DBConfigurations

# Create a SQLAlchemy database engine
engine = create_engine(
    DBConfigurations.sql_alchemy_url, # Database connection URL from configurations
    pool_recycle=3600, # Recycle connections after 1 hour
    echo=False, # Disable SQL query logging for production
)

# Create a SQLAlchemy session
SessionLocal = sessionmaker(autoflush=False, bind=engine)


@contextmanager
def get_context_db():
    """Provides a database session using a context manager.
    
    - Ensures proper session handling (automatic rollback on failure).
    - Closes the session after execution.
    
    Yields:
        Session: A SQLAlchemy database session.
    
    Raises:
        Exception: If an error occurs, the transaction is rolled back before re-raising the exception.
    """
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
