"""
Model Context Protocol (MCP) Server for AI Chatbot Integration
"""
from typing import Dict, Any, List, Optional
from src.models import Task, TaskCreate, TaskUpdate, Conversation, Message
from src.database import get_session, get_session_context
from sqlmodel import select
from uuid import UUID
import re
from datetime import datetime


class MCPServer:
    """
    MCP Server that exposes task operations as tools for the OpenAI Agent.
    """

    def __init__(self):
        self.tools = {
            "add_task": self.add_task,
            "list_tasks": self.list_tasks,
            "complete_task": self.complete_task,
            "update_task": self.update_task,
            "delete_task": self.delete_task,
            "mark_all_tasks": self.mark_all_tasks,
            "delete_all_tasks": self.delete_all_tasks,
            "update_multiple_tasks": self.update_multiple_tasks,
            "uncomplete_task": self.uncomplete_task,
            "bulk_uncomplete_tasks": self.bulk_uncomplete_tasks,
            "bulk_delete_tasks": self.bulk_delete_tasks,
            "bulk_update_tasks": self.bulk_update_tasks
        }

    def _get_validated_user_uuid(self, user_id: str) -> UUID:
        try:
            return UUID(user_id) if isinstance(user_id, str) else user_id
        except ValueError:
            if isinstance(user_id, str) and re.fullmatch(r'[0-9a-f]{32}', user_id):
                formatted_uuid = f"{user_id[:8]}-{user_id[8:12]}-{user_id[12:16]}-{user_id[16:20]}-{user_id[20:]}"
                return UUID(formatted_uuid)
            raise ValueError("Invalid user_id format")

    def add_task(
        self,
        title: str,
        description: Optional[str] = None,
        user_id: str = None,
        priority: str = "medium",
        due_date: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> Dict[str, Any]:

        if not user_id:
            raise ValueError("User ID is required")

        parsed_due_date = None
        if due_date:
            try:
                parsed_due_date = datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                parsed_due_date = None

        with get_session_context() as session:
            task = Task(
                title=title,
                description=description,
                priority=priority,
                due_date=parsed_due_date,
                tags=tags or [],
                user_id=self._get_validated_user_uuid(user_id)
            )
            session.add(task)
            session.commit()
            session.refresh(task)
            return {"task_id": str(task.id), "title": task.title}

    def list_tasks(self, user_id: str) -> List[Dict[str, Any]]:
        user_uuid = self._get_validated_user_uuid(user_id)
        with get_session_context() as session:
            tasks = session.exec(
                select(Task).where(Task.user_id == user_uuid)
            ).all()
            return [
                {
                    "task_id": str(t.id),
                    "title": t.title,
                    "completed": t.completed
                }
                for t in tasks
            ]

    def complete_task(self, task_id: Optional[str] = None, title: Optional[str] = None, user_id: str = None):
        user_uuid = self._get_validated_user_uuid(user_id)
        with get_session_context() as session:
            stmt = select(Task).where(
                Task.id == int(task_id) if task_id else Task.title == title,
                Task.user_id == user_uuid
            )
            task = session.exec(stmt).first()
            if not task:
                raise ValueError("Task not found")
            task.completed = True
            task.completed_at = datetime.utcnow()
            session.commit()
            return {"success": True}

    def uncomplete_task(self, task_id: Optional[str] = None, title: Optional[str] = None, user_id: str = None):
        user_uuid = self._get_validated_user_uuid(user_id)
        with get_session_context() as session:
            stmt = select(Task).where(
                Task.id == int(task_id) if task_id else Task.title == title,
                Task.user_id == user_uuid
            )
            task = session.exec(stmt).first()
            if not task:
                raise ValueError("Task not found")
            task.completed = False
            task.completed_at = None
            session.commit()
            return {"success": True}

    def update_task(
        self,
        task_id: Optional[str] = None,
        title: Optional[str] = None,
        user_id: str = None,
        new_title: Optional[str] = None,
        **kwargs
    ) -> Dict[str, bool]:
        """
        Update a task's details. Can identify the task by either task_id or title.
        If both are provided, task_id takes precedence.
        The new_title parameter is used to change the task's title.
        """
        user_uuid = self._get_validated_user_uuid(user_id)

        with get_session_context() as session:
            # Build query to find the task
            query_conditions = [Task.user_id == user_uuid]

            if task_id:
                query_conditions.append(Task.id == int(task_id))
            elif title:
                query_conditions.append(Task.title == title)
            else:
                raise ValueError("Either task_id or title must be provided to identify the task to update")

            stmt = select(Task).where(*query_conditions)
            task = session.exec(stmt).first()

            if not task:
                raise ValueError("Task not found")

            # Handle the new_title separately since it's a special case
            if new_title is not None:
                task.title = new_title

            # Update other task fields with provided values
            for key, value in kwargs.items():
                if value is not None and hasattr(task, key):
                    setattr(task, key, value)

            session.commit()
            return {"success": True}

    def delete_task(self, task_id: Optional[str] = None, title: Optional[str] = None, user_id: str = None):
        user_uuid = self._get_validated_user_uuid(user_id)
        with get_session_context() as session:
            stmt = select(Task).where(
                Task.id == int(task_id) if task_id else Task.title == title,
                Task.user_id == user_uuid
            )
            task = session.exec(stmt).first()
            if not task:
                raise ValueError("Task not found")
            session.delete(task)
            session.commit()
            return {"success": True}

    def mark_all_tasks(self, completed: bool, user_id: str):
        user_uuid = self._get_validated_user_uuid(user_id)
        with get_session_context() as session:
            tasks = session.exec(select(Task).where(Task.user_id == user_uuid)).all()
            for t in tasks:
                t.completed = completed
                t.completed_at = datetime.utcnow() if completed else None
            session.commit()
            return {"success": True}

    def delete_all_tasks(self, user_id: str):
        user_uuid = self._get_validated_user_uuid(user_id)
        with get_session_context() as session:
            tasks = session.exec(select(Task).where(Task.user_id == user_uuid)).all()
            for t in tasks:
                session.delete(t)
            session.commit()
            return {"success": True}

    def update_multiple_tasks(self, updates: List[Dict[str, Any]], user_id: str):
        user_uuid = self._get_validated_user_uuid(user_id)
        with get_session_context() as session:
            for u in updates:
                task = session.exec(
                    select(Task).where(Task.id == int(u["task_id"]), Task.user_id == user_uuid)
                ).first()
                if task:
                    task.title = u.get("new_title", task.title)
            session.commit()
            return {"success": True}

    def bulk_uncomplete_tasks(self, tasks: List[Dict[str, Any]], user_id: str):
        user_uuid = self._get_validated_user_uuid(user_id)
        with get_session_context() as session:
            for t in tasks:
                stmt = select(Task).where(
                    Task.id == int(t["task_id"]) if "task_id" in t else Task.title == t["title"],
                    Task.user_id == user_uuid
                )
                task = session.exec(stmt).first()
                if task:
                    task.completed = False
                    task.completed_at = None
            session.commit()
            return {"success": True}

    def bulk_update_tasks(self, updates: List[Dict[str, Any]], user_id: str):
        user_uuid = self._get_validated_user_uuid(user_id)
        with get_session_context() as session:
            for u in updates:
                stmt = select(Task).where(
                    Task.id == int(u["task_id"]) if "task_id" in u else Task.title == u["title"],
                    Task.user_id == user_uuid
                )
                task = session.exec(stmt).first()
                if task:
                    for k, v in u.items():
                        if k not in ["task_id", "title"] and hasattr(task, k):
                            setattr(task, k, v)
                    if 'completed' in u:
                        if u['completed']:
                            task.completed_at = datetime.utcnow()
                        else:
                            task.completed_at = None
            session.commit()
            return {"success": True}

    def bulk_delete_tasks(self, tasks: List[Dict[str, Any]], user_id: str):
        user_uuid = self._get_validated_user_uuid(user_id)
        with get_session_context() as session:
            for t in tasks:
                stmt = select(Task).where(
                    Task.id == int(t["task_id"]) if "task_id" in t else Task.title == t["title"],
                    Task.user_id == user_uuid
                )
                task = session.exec(stmt).first()
                if task:
                    session.delete(task)
            session.commit()
            return {"success": True}


mcp_server = MCPServer()
