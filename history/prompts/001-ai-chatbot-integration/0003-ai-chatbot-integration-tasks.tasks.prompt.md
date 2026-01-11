---
id: 0003
title: AI Chatbot Integration Tasks
stage: tasks
date: 2026-01-06
surface: project
model: Claude Sonnet 4.5
feature: 001-ai-chatbot-integration
branch: 001-ai-chatbot-integration
user: Mahad Khan
command: /sp.tasks
labels: [tasks, planning, mcp, openai-agents, sequential-ids]
links:
  spec: ./../../specs/001-ai-chatbot-integration/spec.md
  ticket:
  adr:
  pr:
files:
  - path: specs/001-ai-chatbot-integration/tasks.md
    action: created
    summary: Complete task list for AI Chatbot Integration with MCP and OpenAI Agents
tests:
  - type: format-validation
    result: pass
    summary: All tasks follow the required checklist format with IDs, story labels, and file paths
---

## Prompt

# Task List: Phase 3 AI Chatbot Integration (Skills Optimized)

**Feature**: AI Chatbot with MCP | **Branch**: `001-ai-chatbot-integration`
**ID Strategy**: Sequential Integers (1, 2, 3...) | **Skill Usage**: Dynamic

## Phase 0: Schema & ID Migration (Sub-Agent: DB-Specialist)
*Requirement: Convert to Integer IDs and add Chat tables.*

- [ ] **T-101**: Update `Task` model in `src/models.py`. Change `id` from `UUID` to `int` (PK, Autoincrement).
- [ ] **T-102**: Add `Conversation` and `Message` models with `int` Primary Keys.
- [ ] **T-103**: **[Skill Trigger]** Run `.claude/skills/validate_models` (or your equivalent DB skill) to ensure SQLModel relationships and Integer sequences are correctly mapped.
- [ ] **T-104**: Generate and apply DB migration to Neon PostgreSQL.

## Phase 1: Stateless MCP Server (Sub-Agent: AI-Architect)
*Requirement: Build the tool-calling interface.*

- [ ] **T-201**: Create `src/mcp/server.py` using Official MCP SDK.
- [ ] **T-202**: Implement tools: `add_task`, `list_tasks`, `complete_task`, `delete_task`.
  - *Constraint*: All tools must accept/return `int` IDs.
- [ ] **T-203**: **[Skill Trigger]** Run `.claude/skills/lint_check` on the new MCP module to ensure it follows your project's coding standards.



## Phase 2: AI Runner & Agent Logic (Sub-Agent: AI-Architect)
*Requirement: Stateless request handling with context.*

- [ ] **T-301**: Implement OpenAI Agents SDK logic in `src/agent/runner.py`.
- [ ] **T-302**: Logic to fetch context from `Message` table based on `conversation_id`.
- [ ] **T-303**: Connect MCP tools to the Agent.
- [ ] **T-304**: **[Skill Trigger]** Use `.claude/skills/test_runner` (if exists) to simulate a tool call from the agent logic.

## Phase 3: API & Frontend Integration (Sub-Agent: Frontend-Dev)
*Requirement: UI matching Phase 2 Dashboard.*

- [ ] **T-401**: Create `POST /api/chat` in FastAPI with Auth protection.
- [ ] **T-402**: Integrate OpenAI ChatKit in `frontend/src/app/dashboard/`.
- [ ] **T-403**: Style Chat interface using existing Tailwind +

## User Input

```text
# Task List: Phase 3 AI Chatbot Integration (Skills Optimized)

**Feature**: AI Chatbot with MCP | **Branch**: `001-ai-chatbot-integration`
**ID Strategy**: Sequential Integers (1, 2, 3...) | **Skill Usage**: Dynamic

## Phase 0: Schema & ID Migration (Sub-Agent: DB-Specialist)
*Requirement: Convert to Integer IDs and add Chat tables.*

- [ ] **T-101**: Update `Task` model in `src/models.py`. Change `id` from `UUID` to `int` (PK, Autoincrement).
- [ ] **T-102**: Add `Conversation` and `Message` models with `int` Primary Keys.
- [ ] **T-103**: **[Skill Trigger]** Run `.claude/skills/validate_models` (or your equivalent DB skill) to ensure SQLModel relationships and Integer sequences are correctly mapped.
- [ ] **T-104**: Generate and apply DB migration to Neon PostgreSQL.

## Phase 1: Stateless MCP Server (Sub-Agent: AI-Architect)
*Requirement: Build the tool-calling interface.*

- [ ] **T-201**: Create `src/mcp/server.py` using Official MCP SDK.
- [ ] **T-202**: Implement tools: `add_task`, `list_tasks`, `complete_task`, `delete_task`.
  - *Constraint*: All tools must accept/return `int` IDs.
- [ ] **T-203**: **[Skill Trigger]** Run `.claude/skills/lint_check` on the new MCP module to ensure it follows your project's coding standards.



## Phase 2: AI Runner & Agent Logic (Sub-Agent: AI-Architect)
*Requirement: Stateless request handling with context.*

- [ ] **T-301**: Implement OpenAI Agents SDK logic in `src/agent/runner.py`.
- [ ] **T-302**: Logic to fetch context from `Message` table based on `conversation_id`.
- [ ] **T-303**: Connect MCP tools to the Agent.
- [ ] **T-304**: **[Skill Trigger]** Use `.claude/skills/test_runner` (if exists) to simulate a tool call from the agent logic.

## Phase 3: API & Frontend Integration (Sub-Agent: Frontend-Dev)
*Requirement: UI matching Phase 2 Dashboard.*

- [ ] **T-401**: Create `POST /api/chat` in FastAPI with Auth protection.
- [ ] **T-402**: Integrate OpenAI ChatKit in `frontend/src/app/dashboard/`.
- [ ] **T-403**: Style Chat interface using existing Tailwind +
```

## Response snapshot

# Task List: AI Chatbot Integration with MCP and OpenAI Agents

**Feature**: AI Chatbot with MCP | **Branch**: `001-ai-chatbot-integration`
**ID Strategy**: Sequential Integers (1, 2, 3...) | **Skill Usage**: Dynamic

## Implementation Strategy

This feature will be implemented in priority order of user stories, with each story being independently testable. The core functionality (US1) will be delivered first as an MVP, followed by conversation context management (US2), and finally security enhancements (US3).

## Phase 1: Setup (Project Initialization)

### Goal
Initialize the project structure and ensure all dependencies are available for the AI Chatbot implementation.

- [ ] T001 Set up backend directory structure: `src/mcp/`, `src/agent/`, `src/routers/chat.py`
- [ ] T002 Set up frontend directory structure: `frontend/src/components/chat/`
- [ ] T003 [P] Install required dependencies: `openai`, `uv` package for MCP SDK
- [ ] T004 [P] Verify existing authentication system is accessible for chat endpoint protection

## Phase 2: Foundational (Blocking Prerequisites)

### Goal
Establish the foundational components that all user stories depend on.

- [ ] T005 Update `Task` model in `backend/src/models.py` to use sequential integer ID (PK, Autoincrement)
- [ ] T006 Add `Conversation` and `Message` models with sequential integer Primary Keys to `backend/src/models.py`
- [ ] T007 [P] Create database migration for new models using Alembic
- [ ] T008 [P] [Skill Trigger] Run `.claude/skills/validate_models` to ensure SQLModel relationships and Integer sequences are correctly mapped
- [ ] T009 [Skill Trigger] Run `.claude/skills/lint_check` on the updated models to ensure code quality
- [ ] T010 Create MCP server foundation in `backend/src/mcp/server.py`

## Phase 3: User Story 1 - Natural Language Task Management (Priority: P1)

### Goal
Enable users to interact with their todo list using natural language commands to add, list, complete, update, and delete tasks.

### Independent Test Criteria
User can add, list, complete, update, and delete tasks using natural language commands like "Add a task to buy groceries", "Show me my tasks", "Mark task 3 as complete", etc.

- [ ] T011 [P] [US1] Implement `add_task` MCP tool in `backend/src/mcp/server.py` with integer ID return
- [ ] T012 [P] [US1] Implement `list_tasks` MCP tool in `backend/src/mcp/server.py` returning tasks with integer IDs
- [ ] T013 [US1] Implement `complete_task` MCP tool in `backend/src/mcp/server.py` accepting integer task ID
- [ ] T014 [P] [US1] Implement `update_task` MCP tool in `backend/src/mcp/server.py` accepting integer task ID
- [ ] T015 [US1] Implement `delete_task` MCP tool in `backend/src/mcp/server.py` accepting integer task ID
- [ ] T016 [US1] Create OpenAI Agent runner in `backend/src/agent/runner.py`
- [ ] T017 [US1] Connect MCP tools to the OpenAI Agent in the runner
- [ ] T018 [US1] Create `POST /api/chat` endpoint in `backend/src/routers/chat.py` with basic functionality
- [ ] T019 [P] [US1] Implement frontend ChatInterface component in `frontend/src/components/chat/ChatInterface.tsx`
- [ ] T020 [P] [US1] Integrate ChatInterface into dashboard page at `frontend/src/app/dashboard/page.tsx`
- [ ] T021 [US1] [Skill Trigger] Run `.claude/skills/test_runner` to verify tool calls work correctly
- [ ] T022 [US1] [Skill Trigger] Run `.claude/skills/lint_check` on new backend modules

### Acceptance Scenarios
1. User can add a task with natural language and see it appear with a sequential integer ID
2. User can list tasks and see them with sequential integer IDs
3. User can complete a task by referencing its integer ID

## Phase 4: User Story 2 - Conversation Context Management (Priority: P2)

### Goal
Enable the AI to maintain context across multiple interactions within a conversation.

### Independent Test Criteria
User can have a multi-turn conversation where the AI remembers the context and can reference previous interactions and tasks.

- [ ] T023 [P] [US2] Enhance `Message` model to support conversation context storage
- [ ] T024 [US2] Implement logic to fetch conversation context from DB in `backend/src/agent/runner.py`
- [ ] T025 [US2] Update chat endpoint to manage conversation state using conversation_id
- [ ] T026 [P] [US2] Implement conversation history retrieval in the agent runner
- [ ] T027 [US2] Add conversation title auto-generation based on content
- [ ] T028 [US2] Update frontend to maintain conversation context across messages
- [ ] T029 [US2] [Skill Trigger] Test multi-turn conversation functionality

### Acceptance Scenarios
1. AI remembers context from previous interactions in the same conversation
2. User can switch between multiple conversations and each maintains its own context

## Phase 5: User Story 3 - Secure Task Access (Priority: P3)

### Goal
Ensure that only authenticated users can access and modify their own tasks through the AI chatbot.

### Independent Test Criteria
User can only see and modify their own tasks, and the AI respects user authentication boundaries.

- [ ] T030 [US3] Update chat endpoint to extract and verify user_id from JWT token
- [ ] T031 [P] [US3] Implement user_id validation in all MCP tools to ensure proper task ownership
- [ ] T032 [US3] Add user_id validation to conversation creation and access
- [ ] T033 [P] [US3] Implement proper user isolation in list_tasks to only return user's tasks
- [ ] T034 [US3] Add authentication middleware verification for chat endpoint
- [ ] T035 [US3] [Skill Trigger] Test that users cannot access other users' tasks
- [ ] T036 [US3] [Skill Trigger] Test that unauthenticated users are prompted to log in

### Acceptance Scenarios
1. Authenticated user can only see and modify their own tasks
2. Unauthenticated users are prompted to log in before accessing the chatbot

## Phase 6: Polish & Cross-Cutting Concerns

### Goal
Add error handling, edge case management, and finalize the UI/UX.

- [ ] T037 [P] Add comprehensive error handling for MCP tools
- [ ] T038 Handle edge case: task ID that doesn't exist in tool calls
- [ ] T039 [P] Handle edge case: malformed natural language requests
- [ ] T040 Add retry logic for when AI service is temporarily unavailable
- [ ] T041 [P] Implement proper message streaming in frontend for better UX
- [ ] T042 Add loading states and error messages to ChatInterface
- [ ] T043 [P] Style chat interface to match existing dashboard theme with Tailwind CSS
- [ ] T044 [P] [Skill Trigger] Run comprehensive linting on all new files
- [ ] T045 [Skill Trigger] Run full integration tests to verify concurrent UI and AI modifications work correctly

## Dependencies

- US2 (Conversation Context) depends on US1 (Task Management) foundational components
- US3 (Security) can be implemented in parallel with US1 and US2 since it adds validation layers

## Parallel Execution Opportunities

- Backend MCP tools (T011-T015) can be developed in parallel [P]
- Frontend components (T019) can be developed in parallel with backend API [P]
- Model validation (T008) and linting (T009) can run in parallel [P]
- Multiple conversation context features (T023, T025) can be developed in parallel [P]
- Security validations (T031, T033) can be implemented in parallel [P]

## Outcome

- ✅ Impact: Complete task list generated with 45 specific, actionable tasks organized by user story priority
- 🧪 Tests: All tasks follow required checklist format with IDs, story labels, and file paths
- 📁 Files: Created tasks.md with comprehensive task breakdown aligned to user stories
- 🔁 Next prompts: Ready for /sp.implement to execute tasks
- 🧠 Reflection: Tasks organized by user story priority with clear dependencies and parallel execution opportunities

## Evaluation notes (flywheel)

- Failure modes observed: None - all tasks properly formatted and organized by priority
- Graders run and results (PASS/FAIL): PASS - all tasks follow checklist format requirements
- Prompt variant (if applicable): Standard /sp.tasks workflow with story-based organization
- Next experiment (smallest change to try): Begin implementation with Phase 3 (US1) tasks
