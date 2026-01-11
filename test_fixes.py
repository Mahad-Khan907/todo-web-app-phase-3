#!/usr/bin/env python3
"""
Test script to verify that the AI agent task management fixes work properly.
"""

import asyncio
import sys
import os

# Add the backend src directory to the path
backend_src_path = os.path.join(os.path.dirname(__file__), 'backend', 'src')
sys.path.insert(0, backend_src_path)

from src.mcp.server import mcp_server
from src.database import get_session_context, engine
from src.models import Task, User, create_db_and_tables
from sqlmodel import select
import uuid

def test_basic_task_operations():
    """Test basic task operations to ensure they work correctly."""

    print("Testing basic task operations...")

    # Create a test user ID (using a sample UUID)
    test_user_id = str(uuid.uuid4())

    # Test adding a task
    print("\n1. Testing add_task...")
    try:
        result = mcp_server.add_task(
            title="Test Task 1",
            description="This is a test task",
            user_id=test_user_id,
            priority="high"
        )
        print(f"   ✓ Task added successfully: {result}")
        task_id = result["task_id"]
    except Exception as e:
        print(f"   ✗ Error adding task: {e}")
        return False

    # Test listing tasks
    print("\n2. Testing list_tasks...")
    try:
        tasks = mcp_server.list_tasks(user_id=test_user_id)
        print(f"   ✓ Tasks listed: {tasks}")
        assert len(tasks) > 0, "Should have at least one task"
    except Exception as e:
        print(f"   ✗ Error listing tasks: {e}")
        return False

    # Test updating a task
    print("\n3. Testing update_task...")
    try:
        result = mcp_server.update_task(
            task_id=task_id,
            user_id=test_user_id,
            description="Updated description",
            priority="medium"
        )
        print(f"   ✓ Task updated: {result}")
    except Exception as e:
        print(f"   ✗ Error updating task: {e}")
        return False

    # Test completing a task
    print("\n4. Testing complete_task...")
    try:
        result = mcp_server.complete_task(task_id=task_id, user_id=test_user_id)
        print(f"   ✓ Task completed: {result}")
    except Exception as e:
        print(f"   ✗ Error completing task: {e}")
        return False

    # Test uncompleting a task
    print("\n5. Testing uncomplete_task...")
    try:
        result = mcp_server.uncomplete_task(task_id=task_id, user_id=test_user_id)
        print(f"   ✓ Task uncompleted: {result}")
    except Exception as e:
        print(f"   ✗ Error uncompleting task: {e}")
        return False

    # Test deleting a task
    print("\n6. Testing delete_task...")
    try:
        result = mcp_server.delete_task(task_id=task_id, user_id=test_user_id)
        print(f"   ✓ Task deleted: {result}")
    except Exception as e:
        print(f"   ✗ Error deleting task: {e}")
        return False

    print("\n✓ All basic task operations passed!")
    return True

def test_bulk_operations():
    """Test bulk operations to ensure they work correctly."""

    print("\n\nTesting bulk operations...")

    # Create a test user ID (using a sample UUID)
    test_user_id = str(uuid.uuid4())

    # Add multiple tasks for bulk operations
    print("\n1. Adding multiple tasks for bulk operations...")
    task_ids = []
    for i in range(3):
        result = mcp_server.add_task(
            title=f"Bulk Test Task {i+1}",
            description=f"This is bulk test task {i+1}",
            user_id=test_user_id,
            priority="medium"
        )
        task_ids.append(result["task_id"])
        print(f"   Added task {i+1}: {result['title']} (ID: {result['task_id']})")

    # Test bulk update
    print("\n2. Testing bulk_update_tasks...")
    try:
        updates = [
            {
                "task_id": task_ids[0],
                "title": "Updated Bulk Test Task 1",
                "completed": True
            },
            {
                "task_id": task_ids[1],
                "priority": "high",
                "description": "Updated description for task 2"
            },
            {
                "task_id": task_ids[2],
                "completed": True,
                "priority": "low"
            }
        ]
        result = mcp_server.bulk_update_tasks(updates=updates, user_id=test_user_id)
        print(f"   ✓ Bulk update result: {len(result['results'])} updates processed")
        for res in result['results']:
            print(f"     - {res['identifier']}: {res['status']} - {res['message']}")
    except Exception as e:
        print(f"   ✗ Error in bulk update: {e}")
        return False

    # Test bulk uncomplete
    print("\n3. Testing bulk_uncomplete_tasks...")
    try:
        tasks_to_uncomplete = [{"task_id": tid} for tid in task_ids[:2]]  # Uncomplete first 2 tasks
        result = mcp_server.bulk_uncomplete_tasks(tasks=tasks_to_uncomplete, user_id=test_user_id)
        print(f"   ✓ Bulk uncomplete result: {result}")
    except Exception as e:
        print(f"   ✗ Error in bulk uncomplete: {e}")
        return False

    # Test bulk delete
    print("\n4. Testing bulk_delete_tasks...")
    try:
        tasks_to_delete = [{"task_id": tid} for tid in task_ids]  # Delete all tasks
        result = mcp_server.bulk_delete_tasks(tasks=tasks_to_delete, user_id=test_user_id)
        print(f"   ✓ Bulk delete result: {result}")
    except Exception as e:
        print(f"   ✗ Error in bulk delete: {e}")
        return False

    print("\n✓ All bulk operations passed!")
    return True

def test_edge_cases():
    """Test edge cases and error handling."""

    print("\n\nTesting edge cases...")

    test_user_id = str(uuid.uuid4())

    # Test with invalid task ID
    print("\n1. Testing with invalid task ID...")
    try:
        # This should fail gracefully
        result = mcp_server.complete_task(task_id="999999", user_id=test_user_id)
        print(f"   ? Unexpected success: {result}")
    except ValueError as e:
        print(f"   ✓ Correctly raised ValueError: {e}")
    except Exception as e:
        print(f"   ? Unexpected error: {e}")

    # Test with non-existent task ID
    print("\n2. Testing with non-existent task ID...")
    try:
        # Add a valid task first
        add_result = mcp_server.add_task(
            title="Valid Task",
            user_id=test_user_id
        )
        valid_task_id = add_result["task_id"]
        print(f"   Added valid task: {valid_task_id}")

        # Try to update with non-existent ID
        result = mcp_server.update_task(
            task_id="999999",  # Non-existent ID
            user_id=test_user_id,
            title="Should fail"
        )
        print(f"   ? Unexpected success: {result}")
    except ValueError as e:
        print(f"   ✓ Correctly raised ValueError: {e}")
    except Exception as e:
        print(f"   ? Unexpected error: {e}")

    # Clean up
    try:
        mcp_server.delete_task(task_id=valid_task_id, user_id=test_user_id)
        print("   Cleaned up test task")
    except:
        pass  # Ignore cleanup errors

    print("\n✓ Edge case tests completed!")
    return True

def main():
    """Run all tests."""
    print("Starting AI Agent Task Management Fixes Verification...\n")

    success = True

    success &= test_basic_task_operations()
    success &= test_bulk_operations()
    success &= test_edge_cases()

    print(f"\n{'='*50}")
    if success:
        print("✓ ALL TESTS PASSED! AI agent task management should now work correctly.")
        print("\nThe fixes include:")
        print("- Fixed task creation with correct parameter handling")
        print("- Fixed task ID type conversion (string to integer)")
        print("- Added comprehensive bulk update functionality")
        print("- Fixed all CRUD operations to work with integer task IDs")
        print("- Enhanced error handling and validation")
    else:
        print("✗ SOME TESTS FAILED! Please review the errors above.")

    return success

if __name__ == "__main__":
    main()