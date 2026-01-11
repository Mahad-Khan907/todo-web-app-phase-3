#!/usr/bin/env python3
"""
Helper script to update task 2 with the specified details:
- title = mahad
- description = meow
- tags = mahad
- date = 2026-01-01
- priority = high
"""

import sys
import os
from datetime import datetime
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

from sqlmodel import select
from src.database import get_session_context
from src.models import Task
from uuid import UUID


def update_second_task(user_id_str):
    """
    Updates the 2nd task for the given user with the specified details.
    """
    user_uuid = UUID(user_id_str) if not isinstance(user_id_str, UUID) else user_uuid

    with get_session_context() as session:
        # Get all tasks for the user ordered by ID
        stmt = select(Task).where(Task.user_id == user_uuid).order_by(Task.id)
        tasks = session.exec(stmt).all()

        if len(tasks) < 2:
            print(f"Error: User only has {len(tasks)} task(s). Need at least 2 tasks to update the 2nd one.")
            return False

        # Get the 2nd task (index 1)
        target_task = tasks[1]  # 2nd task (0-indexed)

        print(f"Updating task with ID {target_task.id}: '{target_task.title}' -> 'mahad'")

        # Update the task with the specified details
        target_task.title = "mahad"
        target_task.description = "meow"
        target_task.tags = ["mahad"]  # Set tags as a list
        target_task.priority = "high"
        target_task.due_date = datetime.strptime("2026-01-01", "%Y-%m-%d")

        session.add(target_task)
        session.commit()

        print(f"Successfully updated task {target_task.id}")
        print(f"New details:")
        print(f"  Title: {target_task.title}")
        print(f"  Description: {target_task.description}")
        print(f"  Tags: {target_task.tags}")
        print(f"  Priority: {target_task.priority}")
        print(f"  Due Date: {target_task.due_date}")

        return True


def update_task_by_title(old_title, user_id_str):
    """
    Alternative approach: Updates a task by its current title.
    """
    user_uuid = UUID(user_id_str) if not isinstance(user_id_str, UUID) else user_uuid

    with get_session_context() as session:
        # Find task by title
        stmt = select(Task).where(
            Task.user_id == user_uuid,
            Task.title == old_title
        )
        task = session.exec(stmt).first()

        if not task:
            print(f"Error: Task with title '{old_title}' not found for user {user_id_str}")
            return False

        print(f"Updating task with ID {task.id}: '{task.title}' -> 'mahad'")

        # Update the task with the specified details
        task.title = "mahad"
        task.description = "meow"
        task.tags = ["mahad"]  # Set tags as a list
        task.priority = "high"
        task.due_date = datetime.strptime("2026-01-01", "%Y-%m-%d")

        session.add(task)
        session.commit()

        print(f"Successfully updated task {task.id}")
        print(f"New details:")
        print(f"  Title: {task.title}")
        print(f"  Description: {task.description}")
        print(f"  Tags: {task.tags}")
        print(f"  Priority: {task.priority}")
        print(f"  Due Date: {task.due_date}")

        return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python update_task_helper.py <user_id> [old_title]")
        print("  user_id: The UUID of the user whose task to update")
        print("  old_title: (Optional) The current title of the task to update")
        print("\nExamples:")
        print("  python update_task_helper.py 123e4567-e89b-12d3-a456-426614174000")
        print("  python update_task_helper.py 123e4567-e89b-12d3-a456-426614174000 'Old Task Title'")
        sys.exit(1)

    user_id = sys.argv[1]

    if len(sys.argv) > 2:
        # Update by title
        old_title = sys.argv[2]
        success = update_task_by_title(old_title, user_id)
    else:
        # Update the 2nd task
        success = update_second_task(user_id)

    if not success:
        sys.exit(1)