from sqlmodel import create_engine, Session, SQLModel
from typing import Generator
from contextlib import contextmanager
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")  # Default to local SQLite file

# Create the database engine with better connection pooling for PostgreSQL
connect_args = {}
if DATABASE_URL.startswith("postgresql"):
    # PostgreSQL connection arguments for better connection handling
    connect_args = {
        "connect_timeout": 10,
    }
else:
    connect_args = {"check_same_thread": False}

try:
    # For PostgreSQL, we need to configure pooling at the engine level, not in connect_args
    if DATABASE_URL.startswith("postgresql"):
        engine = create_engine(
            DATABASE_URL,
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True,  # Verify connections before use
            pool_recycle=300,    # Recycle connections after 5 minutes
            connect_args=connect_args
        )
        print("Database engine created for PostgreSQL with connection pooling")
    else:
        engine = create_engine(DATABASE_URL, connect_args=connect_args)
        print("Database engine created for SQLite")
except Exception as e:
    print(f"Failed to create database engine: {e}")
    # Fallback to SQLite
    DATABASE_URL = "sqlite:///./todo_app_fallback.db"
    connect_args = {"check_same_thread": False}
    engine = create_engine(DATABASE_URL, connect_args=connect_args)
    print("Using fallback SQLite database")

def create_db_and_tables():
    """
    Create database tables.
    This function should be called on application startup.
    """
    from .models import User, Task  # Import here to avoid circular imports
    try:
        SQLModel.metadata.create_all(engine)
        print("Database tables created successfully!")
    except Exception as e:
        print(f"Warning: Could not create database tables: {e}")
        print("This might be due to database connection issues.")
        print(f"Attempting to connect to: {DATABASE_URL.split('@')[1].split('/')[0] if '@' in DATABASE_URL and '/' in DATABASE_URL else DATABASE_URL}")

def get_session() -> Generator[Session, None, None]:
    """
    Get a database session.
    This function is used as a FastAPI dependency.
    """
    try:
        with Session(engine) as session:
            yield session
    except Exception as e:
        # Log more detailed error info to help with debugging
        import traceback
        error_msg = str(e)
        if "badly formed hexadecimal UUID string" in error_msg.lower():
            print(f"Database session error: {error_msg}")
            print(f"This error typically occurs when a malformed UUID string is passed to the database.")
            print(f"Check that all UUID strings follow the format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
        else:
            print(f"Database session error: {error_msg}")
        # Print stack trace for debugging
        traceback.print_exc()
        raise e  # Re-raise the exception to be handled by the caller

@contextmanager
def get_session_context():
    """
    Get a database session as a context manager.
    Useful for non-FastAPI contexts.
    """
    try:
        with Session(engine) as session:
            yield session
    except Exception as e:
        # Log more detailed error info to help with debugging
        import traceback
        error_msg = str(e)
        if "badly formed hexadecimal UUID string" in error_msg.lower():
            print(f"Database session context error: {error_msg}")
            print(f"This error typically occurs when a malformed UUID string is passed to the database.")
            print(f"Check that all UUID strings follow the format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
        else:
            print(f"Database session context error: {error_msg}")
        # Print stack trace for debugging
        traceback.print_exc()
        raise e  # Re-raise the exception to be handled by the caller