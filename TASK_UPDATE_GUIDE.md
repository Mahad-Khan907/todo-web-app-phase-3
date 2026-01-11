# Task Update Functionality Guide

## Fixed Update Task Implementation

The `update_task` functionality in the MCP server has been fixed to properly handle updates to task title, description, tags, and other fields.

### Key Changes Made:

1. **Simplified Logic**: Removed the confusing `new_title` parameter requirement
2. **Proper Field Updates**: All task fields (title, description, tags, priority, due_date, etc.) can now be updated directly
3. **Better Error Handling**: Clearer error messages when tasks are not found
4. **Flexible Identification**: Tasks can be identified by either `task_id` or `title`

### How to Update Tasks

#### Method 1: Using the AI Chatbot
When using the chatbot, you can now update tasks with natural language like:
- "Update task 'old title' to have title 'new title', description 'new description', priority 'high', and tags ['tag1', 'tag2']"
- "Change the due date of task 'my task' to 2026-01-01"
- "Update task with title 'todo' to have high priority and tags ['important']"

**Important**: The system distinguishes between identifying a task and changing its title:
- Use the `title` parameter to identify which task to update
- Use the `new_title` parameter to change the task's title

For example: "Update task 'current title' to have new title 'new title'" will find the task with 'current title' and change its title to 'new title'.

#### Method 2: Using the Helper Script
A helper script `update_task_helper.py` is available to update tasks directly:

```bash
# Update the 2nd task for a user
python update_task_helper.py <user_id>

# Update a specific task by its current title
python update_task_helper.py <user_id> "Current Task Title"
```

#### Method 3: Direct API Call
The API endpoint `/tasks/{task_id}` with PATCH method can update any task field:

```json
{
  "title": "new title",
  "description": "new description",
  "priority": "high",
  "due_date": "2026-01-01T00:00:00",
  "tags": ["mahad"]
}
```

### Example Usage for Your Request

To update task 2 with:
- Title = mahad
- Description = meow
- Tags = mahad
- Date = 2026-01-01
- Priority = high

The AI chatbot will now properly handle requests like:
- "Update the second task to have title 'mahad', description 'meow', tags 'mahad', due date '2026-01-01', and priority 'high'"
- Or if you know the current title: "Update task 'current title' to have title 'mahad', description 'meow', tags 'mahad', due date '2026-01-01', and priority 'high'"

### Fields That Can Be Updated

- `new_title`: New title for the task (string, when using AI chatbot)
- `description`: Task description (string, optional)
- `completed`: Completion status (boolean)
- `priority`: Priority level ("low", "medium", or "high")
- `due_date`: Due date in YYYY-MM-DD format
- `tags`: Array of tag strings