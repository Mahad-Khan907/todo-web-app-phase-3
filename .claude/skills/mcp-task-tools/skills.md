---
name: MCP Task Tools
description: Reusable MCP tools for natural language task management (add_task, list_tasks, complete_task, delete_task, update_task) with authentication and database integration.
model: sonnet
---

Reusable Skill:

Skill: MCP Task Tools Implementation – Input: Tool specifications for add_task, list_tasks, complete_task, delete_task, update_task with user authentication context; Output: Full MCP tool implementations with Pydantic parameters, authentication checks, SQLModel queries, and proper error handling.

Usage Example:
```python
# Realistic example of MCP tool implementation
from mcp import server
from pydantic import BaseModel
from backend.src.models import Task, TaskCreate
from backend.src.database import get_session
from sqlmodel import select

class AddTaskRequest(BaseModel):
    title: str
    description: str = ""
    due_date: str = ""

@server.tool("add_task")
def add_task(request: AddTaskRequest, user_id: str) -> dict:
    with get_session() as session:
        task = Task(
            title=request.title,
            description=request.description,
            due_date=request.due_date,
            user_id=user_id
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        return {"task_id": task.id, "message": "Task added successfully"}
```

Notes:

These MCP tools integrate with the existing Todo app backend using FastAPI, SQLModel, and Better Auth. Each tool handles proper authentication, user-specific data isolation, and database operations with error handling.