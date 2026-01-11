#!/usr/bin/env python3
"""
Test script to verify database connection and table creation
"""
import os
import sys
from dotenv import load_dotenv
load_dotenv()

# Add the src directory to the path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.database import engine, get_session
from src.models import SQLModel, User, Task, Conversation, Message
from sqlmodel import select

def test_db_connection():
    print("Testing database connection...")

    # Print the DATABASE_URL being used (without the password for security)
    database_url = os.getenv("DATABASE_URL")
    if database_url and "postgresql" in database_url:
        print("Using PostgreSQL database")
        # Show just the beginning to confirm it's PostgreSQL
        print(f"Database URL starts with: {database_url[:20]}...")
    else:
        print("Using SQLite database")

    try:
        # Try to connect and list tables
        print("\nTesting connection...")
        # Use the context manager function instead
        from src.database import get_session_context
        with get_session_context() as session:
            print("Connection successful!")

            # Check if tables exist by trying to query them
            try:
                # Check if User table exists by counting records
                user_count = session.exec(select(User)).all()
                print(f"Users table exists, found {len(user_count)} users")
            except Exception as e:
                print(f"Users table issue: {e}")

            try:
                # Check if Task table exists by counting records
                task_count = session.exec(select(Task)).all()
                print(f"Tasks table exists, found {len(task_count)} tasks")
            except Exception as e:
                print(f"Tasks table issue: {e}")

            try:
                # Check if Conversation table exists by counting records
                conv_count = session.exec(select(Conversation)).all()
                print(f"Conversations table exists, found {len(conv_count)} conversations")
            except Exception as e:
                print(f"Conversations table issue: {e}")

            try:
                # Check if Message table exists by counting records
                msg_count = session.exec(select(Message)).all()
                print(f"Messages table exists, found {len(msg_count)} messages")
            except Exception as e:
                print(f"Messages table issue: {e}")

        print("\nDatabase connection test completed successfully!")

    except Exception as e:
        print(f"Database connection failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_db_connection()