---
name: Stateless Chat Handler
description: Reusable stateless FastAPI chat endpoint for natural language task management with authentication and OpenAI integration.
model: sonnet
---

Reusable Skill:

Skill: Stateless Chat Endpoint – Input: User message, authentication context, and conversation history; Output: Full FastAPI /api/chat endpoint implementation with authentication, OpenAI integration, streaming support, and proper error handling.

Usage Example:
```python
# Realistic example of stateless chat endpoint
from fastapi import APIRouter, Depends, Request
from backend.src.auth import get_current_user
from backend.src.models import User
from pydantic import BaseModel

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    conversation_id: str = None

@router.post("/api/chat")
async def chat(
    request: ChatRequest,
    user: User = Depends(get_current_user),
    agent: TaskManagementAgent = Depends(get_agent)
):
    response = await agent.run_conversation(request.message, str(user.id))

    # Store conversation in DB
    await store_conversation(user.id, request.message, response)

    return {"response": response, "conversation_id": response.conversation_id}
```

Notes:

This endpoint is stateless and handles authentication via Better Auth, integrates with OpenAI Agents, stores conversation history in the database, and supports both streaming and standard responses. Properly validates inputs and handles errors gracefully.