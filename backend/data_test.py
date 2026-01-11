#!/usr/bin/env python3
"""
Test script to verify data operations work correctly with PostgreSQL
"""
import os
import sys
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()

# Add the src directory to the path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.database import get_session_context
from src.models import User, Task, Conversation, Message
from sqlmodel import select

def test_data_operations():
    print("Testing data operations...")

    # Print the DATABASE_URL being used (without the password for security)
    database_url = os.getenv("DATABASE_URL")
    if database_url and "postgresql" in database_url:
        print("Using PostgreSQL database")
    else:
        print("Using SQLite database")

    try:
        # Test creating and reading data
        print("\nTesting data creation and retrieval...")

        with get_session_context() as session:
            print("Connection successful!")

            # First, let's check if there are any existing users we can use for testing
            # or create a test user directly in the database bypassing password hashing
            print("\n1. Checking for existing users...")
            users = session.exec(select(User)).all()
            if users:
                test_user = users[0]
                print(f"Using existing user with ID: {test_user.id}, email: {test_user.email}")
            else:
                # Create a test user directly with pre-hashed password to avoid bcrypt issues
                print("No existing users found, creating test user...")
                # Using a pre-hashed password (this is 'testpass' hashed with bcrypt)
                prehashed_password = "$2b$12$VcCDgh2tA6/J.o.bh8H45.nN/u21L.KDwYzNm.FN8/J3tk8bDWyrm"  # bcrypt hash for 'testpass'
                test_user = User(
                    email="test@example.com",
                    hashed_password=prehashed_password,
                    full_name="Test User"
                )
                session.add(test_user)
                session.commit()
                session.refresh(test_user)
                print(f"Created test user with ID: {test_user.id}, email: {test_user.email}")

            # Create a test task for the user
            print("\n2. Creating a test task...")
            test_task = Task(
                user_id=test_user.id,
                title="Test Task",
                description="This is a test task",
                status="pending"
            )
            session.add(test_task)
            session.commit()
            session.refresh(test_task)
            print(f"Created task with ID: {test_task.id}, title: {test_task.title}")

            # Create a test conversation for the user
            print("\n3. Creating a test conversation...")
            test_conversation = Conversation(
                user_id=test_user.id,
                title="Test Conversation"
            )
            session.add(test_conversation)
            session.commit()
            session.refresh(test_conversation)
            print(f"Created conversation with ID: {test_conversation.id}, title: {test_conversation.title}")

            # Create a test message in the conversation
            print("\n4. Creating a test message...")
            test_message = Message(
                conversation_id=test_conversation.id,
                user_id=test_user.id,
                role="user",
                content="Hello, this is a test message!"
            )
            session.add(test_message)
            session.commit()
            session.refresh(test_message)
            print(f"Created message with ID: {test_message.id}, content: {test_message.content}")

            # Now read the data back to verify it was stored
            print("\n5. Reading data back from database...")

            # Get all tasks for the user
            tasks = session.exec(select(Task).where(Task.user_id == test_user.id)).all()
            print(f"Found {len(tasks)} tasks for user")
            for task in tasks:
                print(f"  Task ID={task.id}, title={task.title}, completed={task.completed}")

            # Get all conversations for the user
            conversations = session.exec(select(Conversation).where(Conversation.user_id == test_user.id)).all()
            print(f"Found {len(conversations)} conversations for user")
            for conv in conversations:
                print(f"  Conversation ID={conv.id}, title={conv.title}")

            # Get all messages in the conversation
            messages = session.exec(select(Message).where(Message.conversation_id == test_conversation.id)).all()
            print(f"Found {len(messages)} messages in conversation")
            for msg in messages:
                print(f"  Message ID={msg.id}, role={msg.role}, content={msg.content}")

            print("\nData operations test completed successfully!")

            # Clean up: delete test data (only if we created the test user)
            if not users:  # Only delete if we created a new test user
                print("\n6. Cleaning up test data...")
                session.delete(test_message)
                session.delete(test_task)
                session.delete(test_conversation)
                session.delete(test_user)
                session.commit()
                print("Test data cleaned up successfully!")

    except Exception as e:
        print(f"Data operations test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_data_operations()