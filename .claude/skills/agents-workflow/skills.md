---
name: Agents Workflow
description: Reusable OpenAI Agents workflow for natural language task management with MCP tool integration and confirmation flows.
model: sonnet
---

Reusable Skill:

Skill: OpenAI Agents Workflow – Input: Natural language query, user context, and MCP tools configuration; Output: Full OpenAI Agent runner implementation with tool integration, natural language processing, confirmation flows, and structured response formatting.

Usage Example:
```python
# Realistic example of OpenAI Agents implementation
from openai import OpenAI
from backend.src.auth import get_current_user
import json

class TaskManagementAgent:
    def __init__(self, client: OpenAI, tools: list):
        self.client = client
        self.tools = tools

    async def run_conversation(self, user_input: str, user_id: str):
        response = self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": user_input}],
            tools=self.tools,
            user=str(user_id)
        )

        # Process tool calls and return structured response
        return self.process_tool_calls(response)
```

Notes:

This workflow handles natural language understanding, routes appropriate tasks to MCP tools, manages confirmation flows for destructive operations, and formats responses for the chat interface. Includes proper error handling and authentication integration.