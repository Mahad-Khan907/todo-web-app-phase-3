"""
OpenAI Agent Runner for AI Chatbot Integration

This module implements the OpenAI Agent logic that connects MCP tools to the agent
and handles stateless request processing with context from the database.
"""
import json
from typing import Optional
from openai import OpenAI, APIError
from src.mcp.server import mcp_server
from src.models import Message, Conversation
from src.database import get_session, get_session_context
from sqlmodel import select
import os
from uuid import UUID
import time


class AgentRunner:
    """
    Runs the OpenAI Agent with MCP tools and manages conversation context.
    """

    def __init__(self):
        # Initialize OpenAI client
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # Get MCP tools
        self.tools = list(mcp_server.tools.values())

        # Map function names to actual functions for tool calling
        self.function_map = {
            "add_task": mcp_server.add_task,
            "list_tasks": mcp_server.list_tasks,
            "complete_task": mcp_server.complete_task,
            "update_task": mcp_server.update_task,
            "delete_task": mcp_server.delete_task,
            "mark_all_tasks": mcp_server.mark_all_tasks,
            "delete_all_tasks": mcp_server.delete_all_tasks,
            "update_multiple_tasks": mcp_server.update_multiple_tasks,
            "uncomplete_task": mcp_server.uncomplete_task,
            "bulk_uncomplete_tasks": mcp_server.bulk_uncomplete_tasks,
            "bulk_delete_tasks": mcp_server.bulk_delete_tasks,
            "bulk_update_tasks": mcp_server.bulk_update_tasks
        }

    def get_conversation_context(
        self,
        conversation_id: int,
        user_id: str,
        limit: int = 10
    ) -> list:
        """
        Fetches the last N messages from a conversation to provide context to the agent.

        Args:
            conversation_id: ID of the conversation
            user_id: ID of the user
            limit: Number of recent messages to fetch

        Returns:
            List of message dictionaries
        """
        with get_session_context() as session:
            # Get the conversation to ensure it belongs to the user - the user_id should be a UUID string that can be converted
            import re
            try:
                # Convert the user_id string to UUID object for comparison
                user_uuid = UUID(user_id)
            except ValueError:
                # If it's not a valid UUID string, check if it's a hex string that needs to be formatted
                # Check if it's a hex string without dashes
                if isinstance(user_id, str) and re.fullmatch(r'[0-9a-f]{32}', user_id):
                    # Format as UUID: 12345678123456781234567812345678 -> 12345678-1234-5678-1234-567812345678
                    formatted_uuid = f"{user_id[:8]}-{user_id[8:12]}-{user_id[12:16]}-{user_id[16:20]}-{user_id[20:]}"
                    user_uuid = UUID(formatted_uuid)
                else:
                    # For security, enforce the original authenticated user_id
                    # This prevents the agent from acting on behalf of other users
                    user_uuid = UUID(user_id)

            user_filter = Conversation.user_id == user_uuid
            conversation_statement = select(Conversation).where(
                Conversation.id == conversation_id,
                user_filter
            )
            conversation = session.exec(conversation_statement).first()

            if not conversation:
                error_msg = f"Conversation with ID {conversation_id} not found " \
                           f"or doesn't belong to user"
                raise ValueError(error_msg)

            # Get recent messages from this conversation
            message_statement = select(Message).where(
                Message.conversation_id == conversation_id
            ).order_by(Message.created_at.desc()).limit(limit)

            messages = session.exec(message_statement).all()

            # Convert to OpenAI message format (reverse order to get chronological)
            context_messages = []
            for msg in reversed(messages):
                context_messages.append({
                    "role": msg.role,
                    "content": msg.content
                })

            return context_messages

    def run_agent(
        self,
        message: str,
        conversation_id: Optional[int],
        user_id: str
    ) -> str:
        """
        Runs the OpenAI Agent with the given message and context.

        Args:
            message: User's input message
            conversation_id: Optional conversation ID (creates new if None)
            user_id: User ID for authentication and data isolation

        Returns:
            Agent's response message
        """
        # Prepare the messages for the agent
        messages = []

        # Add system message to instruct the agent on how to use tools
        messages.append({
            "role": "system",
            "content": (
                "You are a helpful assistant that manages tasks for users. "
                "You can use the following tools to interact with the task system: "
                "add_task, list_tasks, complete_task, update_task, delete_task, "
                "mark_all_tasks, delete_all_tasks, update_multiple_tasks, "
                "uncomplete_task, bulk_uncomplete_tasks, bulk_delete_tasks. "
                "When a user asks to modify a task (e.g., complete, update, delete), "
                "first try to identify the task by its title. If you find a matching task, "
                "use its title to call the appropriate tool. If you cannot find a task "
                "by its title, or if there are multiple tasks with the same title, "
                "ask the user to provide the task ID. "
                "When a user asks to perform a bulk operation on multiple tasks (e.g., 'mark tasks with title A and B as pending'), "
                "use the appropriate bulk operation tool and provide a list of task titles or IDs. For example, to mark tasks with title 'Task 1' and 'Task 2' as pending, "
                "use the `bulk_uncomplete_tasks` tool with `tasks=[{'title': 'Task 1'}, {'title': 'Task 2'}]`. To delete tasks with ID 123 and 456, use the `bulk_delete_tasks` tool with `tasks=[{'task_id': '123'}, {'task_id': '456'}]`. "
                "When a user asks to perform a bulk operation on all tasks (e.g., 'mark all tasks as complete'), use the appropriate `mark_all_tasks` or `delete_all_tasks` tool. "
                "For bulk updates of titles, you must provide a list of updates, "
                "where each update is a dictionary containing the task identifier (task_id or title) and the new title. "
                "Always use the user_id parameter when calling any tool. "
                "When a user wants to add a task, you should be flexible in accepting input formats. "
                "Recognize structured input like 'title = X, desc = Y, priority = Z' or 'title: X, description: Y, priority: Z'. "
                "When extracting information, look for these fields: "
                "1. Title (required) - look for keywords like 'title', 'name', 'task' "
                "2. Description (optional) - look for keywords like 'desc', 'description', 'details' "
                "3. Priority (high, medium, or low) - look for 'priority', 'prio', 'level' "
                "4. Due date (optional, in YYYY-MM-DD format) - look for 'date', 'due', 'deadline' "
                "5. Tags (optional, comma-separated) - look for 'tags', 'labels', 'categories' "
                "When updating a task, distinguish between identifying the task and changing its title: "
                "If a user says 'update task X to Y with description Z', interpret this as updating the task with title X, "
                "changing its title to Y, and setting description to Z. "
                "If a user wants to update properties but keep the same title, they should specify which properties to update. "
                "For example, 'update task prince with description ali, priority high, tag uza, due date 2026-01-01' "
                "should update only those properties while keeping the title as 'prince'. "
                "If the user provides partial information across multiple messages, remember the context and combine the information. "
                "If date is provided in a different format like '8/jan/2026', convert it to YYYY-MM-DD format (e.g., '2026-01-08'). "
                "Be helpful and concise in your responses. "
                "Include context-aware emojis in every response: "
                "✅ for task completion, 🚀 for new tasks, 🕒 for reminders, "
                "📝 for updates, ❌ for deletions, 💬 for general chat, "
                "🔍 for searches/lists, ⏳ for pending actions."
            )
        })

        # Add conversation context if we have an existing conversation
        if conversation_id:
            try:
                context_messages = self.get_conversation_context(
                    conversation_id,
                    user_id
                )
                messages.extend(context_messages)
            except ValueError:
                # If conversation doesn't exist or doesn't belong to user, start fresh
                pass

        # Add the user's current message
        messages.append({
            "role": "user",
            "content": message
        })

        # Call OpenAI API with tools with retry logic
        response = self._call_openai_with_retry(messages)

        # Process the response
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        if tool_calls:
            # Add the assistant's tool calls to messages (this is required for the API to understand the flow)
            # We need to add the assistant message that contains the tool calls
            messages.append({
                "role": "assistant",
                "content": response_message.content,
                "tool_calls": tool_calls
            })

            # Execute tool calls
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                # Add user_id if not present (ensure security)
                if 'user_id' not in function_args:
                    function_args['user_id'] = user_id

                # Execute the function
                if function_name in self.function_map:
                    function_to_call = self.function_map[function_name]
                    try:
                        # Security: Ensure the user_id in function_args is validated as a UUID
                        # This prevents the agent from potentially manipulating the user_id
                        if 'user_id' in function_args:
                            import uuid
                            arg_user_id = function_args['user_id']

                            # Validate that the user_id is a proper UUID string
                            try:
                                # Try to parse as UUID
                                uuid.UUID(arg_user_id)
                            except ValueError:
                                # If it's not a valid UUID string, check if it's a hex string that needs to be formatted
                                import re
                                if isinstance(arg_user_id, str) and re.fullmatch(r'[0-9a-f]{32}', arg_user_id):
                                    # Format as UUID: 12345678123456781234567812345678 -> 12345678-1234-5678-1234-567812345678
                                    formatted_uuid = f"{arg_user_id[:8]}-{arg_user_id[8:12]}-{arg_user_id[12:16]}-{arg_user_id[16:20]}-{arg_user_id[20:]}"
                                    function_args['user_id'] = formatted_uuid
                                else:
                                    # For security, enforce the original authenticated user_id
                                    # This prevents the agent from acting on behalf of other users
                                    function_args['user_id'] = user_id

                        function_response = function_to_call(**function_args)

                        # Add the tool response to messages for the assistant to process
                        messages.append({
                            "role": "tool",
                            "content": str(function_response),
                            "tool_call_id": tool_call.id
                        })
                    except Exception as e:
                        messages.append({
                            "role": "tool",
                            "content": f"Error: {str(e)}",
                            "tool_call_id": tool_call.id
                        })

            # Get final response from assistant after tool execution with retry logic
            final_response = self._call_openai_with_retry(messages, final_call=True)

            return final_response.choices[0].message.content
        else:
            # No tool calls were made, return the assistant's direct response
            return response_message.content

    def _call_openai_with_retry(
        self,
        messages: list,
        final_call: bool = False,
        max_retries: int = 3
    ) -> any:
        """
        Call OpenAI API with retry logic for handling temporary unavailability.

        Args:
            messages: List of messages to send to the API
            final_call: Whether this is a final call after tool execution
            max_retries: Maximum number of retry attempts

        Returns:
            API response
        """
        last_exception = None

        for attempt in range(max_retries):
            try:
                # Prepare tools only for non-final calls
                tools = []
                if not final_call:
                    tools = [
                        {
                            "type": "function",
                            "function": {
                                "name": "add_task",
                                "description": "Add a new task",
                                "parameters": {
                                    "type": "object",
                                    "properties": {
                                        "title": {"type": "string", "description": "Task title"},
                                        "description": {"type": "string", "description": "Task description (optional)"},
                                        "priority": {"type": "string", "description": "Priority level: high, medium, or low", "enum": ["high", "medium", "low"]},
                                        "due_date": {"type": "string", "description": "Due date in YYYY-MM-DD format or format like DD/month/YYYY"},
                                        "tags": {"type": "array", "items": {"type": "string"}, "description": "Array of tags for the task"},
                                        "user_id": {"type": "string", "description": "User ID"}
                                    },
                                    "required": ["title", "user_id"]
                                }
                            }
                        },
                        {
                            "type": "function",
                            "function": {
                                "name": "list_tasks",
                                "description": "List all tasks for the user",
                                "parameters": {
                                    "type": "object",
                                    "properties": {
                                        "user_id": {"type": "string", "description": "User ID"}
                                    },
                                    "required": ["user_id"]
                                }
                            }
                        },
                        {
                            "type": "function",
                            "function": {
                                "name": "complete_task",
                                "description": "Mark a task as completed, identified by its ID or title",
                                "parameters": {
                                    "type": "object",
                                    "properties": {
                                        "task_id": {"type": "string", "description": "ID of the task to complete (optional)"},
                                        "title": {"type": "string", "description": "Title of the task to complete (optional)"},
                                        "user_id": {"type": "string", "description": "User ID"}
                                    },
                                    "required": ["user_id"]
                                }
                            }
                        },
                        {
                            "type": "function",
                            "function": {
                                "name": "update_task",
                                "description": "Update a task's details, identified by its ID or title. The 'title' parameter identifies which task to update, while 'new_title' changes the title. If you want to update other properties but keep the same title, use 'title' to identify the task but don't specify 'new_title'.",
                                "parameters": {
                                    "type": "object",
                                    "properties": {
                                        "task_id": {"type": "string", "description": "ID of the task to update (optional)"},
                                        "title": {"type": "string", "description": "Title of the task to update (used for identification)"},
                                        "user_id": {"type": "string", "description": "User ID"},
                                        "new_title": {"type": "string", "description": "New title for the task (optional - only specify if you want to change the title)"},
                                        "description": {"type": "string", "description": "New description (optional)"},
                                        "completed": {"type": "boolean", "description": "New completion status (optional)"},
                                        "priority": {"type": "string", "description": "Priority level: high, medium, or low", "enum": ["high", "medium", "low"]},
                                        "due_date": {"type": "string", "description": "Due date in YYYY-MM-DD format or format like DD/month/YYYY"},
                                        "tags": {"type": "array", "items": {"type": "string"}, "description": "Array of tags for the task"}
                                    },
                                    "required": ["user_id"]
                                }
                            }
                        },
                        {
                            "type": "function",
                            "function": {
                                "name": "delete_task",
                                "description": "Delete a task, identified by its ID or title",
                                "parameters": {
                                    "type": "object",
                                    "properties": {
                                        "task_id": {"type": "string", "description": "ID of the task to delete (optional)"},
                                        "title": {"type": "string", "description": "Title of the task to delete (optional)"},
                                        "user_id": {"type": "string", "description": "User ID"}
                                    },
                                    "required": ["user_id"]
                                }
                            }
                        },
                        {
                            "type": "function",
                            "function": {
                                "name": "mark_all_tasks",
                                "description": "Mark all tasks as completed or not completed",
                                "parameters": {
                                    "type": "object",
                                    "properties": {
                                        "completed": {"type": "boolean", "description": "The completion status to set for all tasks"},
                                        "user_id": {"type": "string", "description": "User ID"}
                                    },
                                    "required": ["completed", "user_id"]
                                }
                            }
                        },
                        {
                            "type": "function",
                            "function": {
                                "name": "delete_all_tasks",
                                "description": "Delete all tasks for the user",
                                "parameters": {
                                    "type": "object",
                                    "properties": {
                                        "user_id": {"type": "string", "description": "User ID"}
                                    },
                                    "required": ["user_id"]
                                }
                            }
                        },
                        {
                            "type": "function",
                            "function": {
                                "name": "update_multiple_tasks",
                                "description": "Update multiple tasks at once",
                                "parameters": {
                                    "type": "object",
                                    "properties": {
                                        "updates": {
                                            "type": "array",
                                            "items": {
                                                "type": "object",
                                                "properties": {
                                                    "task_id": {"type": "string", "description": "ID of the task to update (optional)"},
                                                    "title": {"type": "string", "description": "Title of the task to update (optional)"},
                                                    "new_title": {"type": "string", "description": "New title for the task"}
                                                },
                                                "required": ["new_title"]
                                            }
                                        },
                                        "user_id": {"type": "string", "description": "User ID"}
                                    },
                                    "required": ["updates", "user_id"]
                                }
                            }
                        },
                        {
                            "type": "function",
                            "function": {
                                "name": "uncomplete_task",
                                "description": "Mark a task as not completed",
                                "parameters": {
                                    "type": "object",
                                    "properties": {
                                        "task_id": {"type": "string", "description": "ID of the task to uncomplete (optional)"},
                                        "title": {"type": "string", "description": "Title of the task to uncomplete (optional)"},
                                        "user_id": {"type": "string", "description": "User ID"}
                                    },
                                    "required": ["user_id"]
                                }
                            }
                        },
                        {
                            "type": "function",
                            "function": {
                                "name": "bulk_uncomplete_tasks",
                                "description": "Mark multiple tasks as not completed",
                                "parameters": {
                                    "type": "object",
                                    "properties": {
                                        "tasks": {
                                            "type": "array",
                                            "items": {
                                                "type": "object",
                                                "properties": {
                                                    "task_id": {"type": "string", "description": "ID of the task to uncomplete (optional)"},
                                                    "title": {"type": "string", "description": "Title of the task to uncomplete (optional)"}
                                                }
                                            },
                                            "description": "A list of tasks to mark as not completed, identified by ID or title"
                                        },
                                        "user_id": {"type": "string", "description": "User ID"}
                                    },
                                    "required": ["tasks", "user_id"]
                                }
                            }
                        },
                        {
                            "type": "function",
                            "function": {
                                "name": "bulk_delete_tasks",
                                "description": "Delete multiple tasks at once",
                                "parameters": {
                                    "type": "object",
                                    "properties": {
                                        "tasks": {
                                            "type": "array",
                                            "items": {
                                                "type": "object",
                                                "properties": {
                                                    "task_id": {"type": "string", "description": "ID of the task to delete (optional)"},
                                                    "title": {"type": "string", "description": "Title of the task to delete (optional)"}
                                                }
                                            },
                                            "description": "A list of tasks to delete, identified by ID or title"
                                        },
                                        "user_id": {"type": "string", "description": "User ID"}
                                    },
                                    "required": ["tasks", "user_id"]
                                }
                            }
                        },
                        {
                            "type": "function",
                            "function": {
                                "name": "bulk_update_tasks",
                                "description": "Update multiple tasks at once with various properties",
                                "parameters": {
                                    "type": "object",
                                    "properties": {
                                        "updates": {
                                            "type": "array",
                                            "items": {
                                                "type": "object",
                                                "properties": {
                                                    "task_id": {"type": "string", "description": "ID of the task to update (optional)"},
                                                    "title": {"type": "string", "description": "Title of the task to update (optional)"},
                                                    "new_title": {"type": "string", "description": "New title for the task (optional)"},
                                                    "description": {"type": "string", "description": "New description (optional)"},
                                                    "completed": {"type": "boolean", "description": "New completion status (optional)"},
                                                    "priority": {"type": "string", "description": "Priority level: high, medium, or low", "enum": ["high", "medium", "low"]},
                                                    "due_date": {"type": "string", "description": "Due date in YYYY-MM-DD format or format like DD/month/YYYY"},
                                                    "tags": {"type": "array", "items": {"type": "string"}, "description": "Array of tags for the task"}
                                                },
                                                "description": "A list of updates to apply to tasks, each identified by ID or title"
                                            },
                                            "description": "A list of updates to apply to multiple tasks"
                                        },
                                        "user_id": {"type": "string", "description": "User ID"}
                                    },
                                    "required": ["updates", "user_id"]
                                }
                            }
                        }
                    ]

                # Make the API call
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",  # Could be configurable
                    messages=messages,
                    tools=tools if tools else None,  # Don't pass tools if it's an empty list for final calls
                    tool_choice="auto" if tools else None
                )

                return response

            except APIError as e:
                last_exception = e
                if attempt < max_retries - 1:  # Don't sleep on the last attempt
                    wait_time = (2 ** attempt) + 1  # Exponential backoff: 1, 3, 7 seconds
                    time.sleep(wait_time)
                else:
                    # If all retries failed, raise the last exception
                    raise last_exception
            except Exception as e:
                # For non-API errors, don't retry
                raise e


# Global agent runner instance
agent_runner = AgentRunner()
