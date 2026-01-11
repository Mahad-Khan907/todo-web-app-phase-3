---
id: 0002
title: AI Chatbot Integration Plan
stage: plan
date: 2026-01-06
surface: project
model: Claude Sonnet 4.5
feature: 001-ai-chatbot-integration
branch: 001-ai-chatbot-integration
user: Mahad Khan
command: /sp.plan
labels: [planning, architecture, mcp, openai-agents]
links:
  spec: ./../../specs/001-ai-chatbot-integration/spec.md
  ticket:
  adr:
  pr:
files:
  - path: specs/001-ai-chatbot-integration/plan.md
    action: created
    summary: Implementation plan for AI Chatbot with MCP and OpenAI Agents
  - path: specs/001-ai-chatbot-integration/research.md
    action: created
    summary: Research on technology decisions and architecture
  - path: specs/001-ai-chatbot-integration/data-model.md
    action: created
    summary: Data model definitions for Task, Conversation, and Message entities
  - path: specs/001-ai-chatbot-integration/contracts/chat-api.yaml
    action: created
    summary: API contract for chat endpoint and MCP tools
  - path: specs/001-ai-chatbot-integration/quickstart.md
    action: created
    summary: Quickstart guide for developers
  - path: CLAUDE.md
    action: updated
    summary: Updated agent context with new technologies
tests:
  - type: compliance
    result: pass
    summary: All constitution checks passed
---

## Prompt

# Implementation Plan: Phase 3 AI Chatbot Integration

**Status**: Planning | **Branch**: `001-ai-chatbot-integration`
**Core Constraint**: Use Sequential Integer IDs (1, 2, 3...) | **Architecture**: Stateless MCP

## 1. Executive Summary
This plan integrates an AI Chatbot into the Phase 2 Todo App. We will leverage the OpenAI Agents SDK and build a custom MCP server. All state is persisted in Neon PostgreSQL to maintain a stateless server environment.

## 2. Technical Context
- **Backend**: FastAPI + SQLModel + Official MCP SDK.
- **AI**: OpenAI Agents SDK (Runner & Agent logic).
- **ID Strategy**: Transition from UUID (if any) to Sequential Integers for Tasks and Conversations.
- **Sub-Agents**: Claude Code will spawn sub-agents for specialized file modifications.

## 3. Implementation Phases

### Phase 0: Database Schema Update (Sub-Agent: DB-Specialist)
- **Task**: Modify `src/models.py`.
- **Changes**:
  - Ensure `Task.id` is `int` with `primary_key=True`.
  - Add `Conversation` model (id: int, user_id: str).
  - Add `Message` model (id: int, conversation_id: int, role: str, content: str).
- **Migration**: Run migrations to ensure sequential IDs start correctly.

### Phase 1: Stateless MCP Server (Sub-Agent: AI-Architect)
- **Task**: Create `src/mcp/server.py`.
- **Tools Implementation**:
  - `add_task`: Saves to DB, returns Integer ID.
  - `list_tasks`: Fetches from DB, filtered by `user_id`.
  - `complete_task`: Updates `completed` status for a specific Integer ID.
  - `delete_task/update_task`: Targeted via Integer IDs.



### Phase 2: Agent Runner & Logic (Sub-Agent: AI-Architect)
- **Task**: Create `src/agent/runner.py`.
- **Logic**:
  - Receive `message` and `conversation_id`.
  - Fetch previous messages for that `conversation_id` from DB.
  - Initialize OpenAI Agent with MCP tools.
  - Execute turn and capture tool calls.

### Phase 3: Chat API Endpoints (Sub-Agent: Backend-Dev)
- **Task**: Create `src/routers/chat.py`.
- **Endpoint**: `POST /api/chat`.
- **Security**: Use existing `get_current_user` dependency to protect the route and enforce `user_id` ownership.

### Phase 4: Frontend UI Integration (Sub-Agent: Frontend-Dev)
- **Task**: Integrate OpenAI ChatKit in `frontend/src/app/dashboard/`.
- **Styling**: Use existing Tailwind config and Shadcn components.
- **Functionality**: Support message streaming and display Task IDs (1, 2, 3) clearly in the chat bubble.

## 4. Skills & Tools Usage
- Use `.claude/` folder skills for:
  - `lint_check`: Run after every backend file modification.
  - `validate_models`: Ensure SQLModel relationships are correct.

## 5. Verification Plan
- **Manual Test**: "Add a task to buy milk" -> Verify DB has ID 1.
- **Natural Language Test**: "Mark task 1 as done" -> Verify tool `complete_task(id=1)` is triggered.
- **Persistence Test**: Restart server -> Verify chat history is still visible in the UI.

## User Input

```text
# Implementation Plan: Phase 3 AI Chatbot Integration

**Status**: Planning | **Branch**: `001-ai-chatbot-integration`
**Core Constraint**: Use Sequential Integer IDs (1, 2, 3...) | **Architecture**: Stateless MCP

## 1. Executive Summary
This plan integrates an AI Chatbot into the Phase 2 Todo App. We will leverage the OpenAI Agents SDK and build a custom MCP server. All state is persisted in Neon PostgreSQL to maintain a stateless server environment.

## 2. Technical Context
- **Backend**: FastAPI + SQLModel + Official MCP SDK.
- **AI**: OpenAI Agents SDK (Runner & Agent logic).
- **ID Strategy**: Transition from UUID (if any) to Sequential Integers for Tasks and Conversations.
- **Sub-Agents**: Claude Code will spawn sub-agents for specialized file modifications.

## 3. Implementation Phases

### Phase 0: Database Schema Update (Sub-Agent: DB-Specialist)
- **Task**: Modify `src/models.py`.
- **Changes**:
  - Ensure `Task.id` is `int` with `primary_key=True`.
  - Add `Conversation` model (id: int, user_id: str).
  - Add `Message` model (id: int, conversation_id: int, role: str, content: str).
- **Migration**: Run migrations to ensure sequential IDs start correctly.

### Phase 1: Stateless MCP Server (Sub-Agent: AI-Architect)
- **Task**: Create `src/mcp/server.py`.
- **Tools Implementation**:
  - `add_task`: Saves to DB, returns Integer ID.
  - `list_tasks`: Fetches from DB, filtered by `user_id`.
  - `complete_task`: Updates `completed` status for a specific Integer ID.
  - `delete_task/update_task`: Targeted via Integer IDs.



### Phase 2: Agent Runner & Logic (Sub-Agent: AI-Architect)
- **Task**: Create `src/agent/runner.py`.
- **Logic**:
  - Receive `message` and `conversation_id`.
  - Fetch previous messages for that `conversation_id` from DB.
  - Initialize OpenAI Agent with MCP tools.
  - Execute turn and capture tool calls.

### Phase 3: Chat API Endpoints (Sub-Agent: Backend-Dev)
- **Task**: Create `src/routers/chat.py`.
- **Endpoint**: `POST /api/chat`.
- **Security**: Use existing `get_current_user` dependency to protect the route and enforce `user_id` ownership.

### Phase 4: Frontend UI Integration (Sub-Agent: Frontend-Dev)
- **Task**: Integrate OpenAI ChatKit in `frontend/src/app/dashboard/`.
- **Styling**: Use existing Tailwind config and Shadcn components.
- **Functionality**: Support message streaming and display Task IDs (1, 2, 3) clearly in the chat bubble.

## 4. Skills & Tools Usage
- Use `.claude/` folder skills for:
  - `lint_check`: Run after every backend file modification.
  - `validate_models`: Ensure SQLModel relationships are correct.

## 5. Verification Plan
- **Manual Test**: "Add a task to buy milk" -> Verify DB has ID 1.
- **Natural Language Test**: "Mark task 1 as done" -> Verify tool `complete_task(id=1)` is triggered.
- **Persistence Test**: Restart server -> Verify chat history is still visible in the UI.
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Setup**: Run `.specify/scripts/bash/setup-plan.sh --json` from repo root and parse JSON for FEATURE_SPEC, IMPL_PLAN, SPECS_DIR, BRANCH. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Load context**: Read FEATURE_SPEC and `.specify/memory/constitution.md`. Load IMPL_PLAN template (already copied).

3. **Execute plan workflow**: Follow the structure in IMPL_PLAN template to:
   - Fill Technical Context (mark unknowns as "NEEDS CLARIFICATION")
   - Fill Constitution Check section from constitution
   - Evaluate gates (ERROR if violations unjustified)
   - Phase 0: Generate research.md (resolve all NEEDS CLARIFICATION)
   - Phase 1: Generate data-model.md, contracts/, quickstart.md
   - Phase 1: Update agent context by running the agent script
   - Re-evaluate Constitution Check post-design

4. **Stop and report**: Command ends after Phase 2 planning. Report branch, IMPL_PLAN path, and generated artifacts.

## Phases

### Phase 0: Outline & Research

1. **Extract unknowns from Technical Context** above:
   - For each NEEDS CLARIFICATION → research task
   - For each dependency → best practices task
   - For each integration → patterns task

2. **Generate and dispatch research agents**:

   ```text
   For each unknown in Technical Context:
     Task: "Research {unknown} for {feature context}"
   For each technology choice:
     Task: "Find best practices for {tech} in {domain}"
   ```

3. **Consolidate findings** in `research.md` using format:
   - Decision: [what was chosen]
   - Rationale: [why chosen]
   - Alternatives considered: [what else evaluated]

**Output**: research.md with all NEEDS CLARIFICATION resolved

### Phase 1: Design & Contracts

**Prerequisites:** `research.md` complete

1. **Extract entities from feature spec** → `data-model.md`:
   - Entity name, fields, relationships
   - Validation rules from requirements
   - State transitions if applicable

2. **Generate API contracts** from functional requirements:
   - For each user action → endpoint
   - Use standard REST/GraphQL patterns
   - Output OpenAPI/GraphQL schema to `/contracts/`

3. **Agent context update**:
   - Run `.specify/scripts/bash/update-agent-context.sh claude`
   - These scripts detect which AI agent is in use
   - Update the appropriate agent-specific context file
   - Add only new technology from current plan
   - Preserve manual additions between markers

**Output**: data-model.md, /contracts/*, quickstart.md, agent-specific file

## Key rules

- Use absolute paths
- ERROR on gate failures or unresolved clarifications

---

As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent‑native tools when possible.

1) Determine Stage
   - Stage: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

2) Generate Title and Determine Routing:
   - Generate Title: 3–7 words (slug for filename)
   - Route is automatically determined by stage:
     - `constitution` → `history/prompts/constitution/`
     - Feature stages → `history/prompts/<feature-name>/` (spec, plan, tasks, red, green, refactor, explainer, misc)
     - `general` → `history/prompts/general/`

3) Create and Fill PHR (Shell first; fallback agent‑native)
   - Run: `.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json`
   - Open the file and fill remaining placeholders (YAML + body), embedding full PROMPT_TEXT (verbatim) and concise RESPONSE_TEXT.
   - If the script fails:
     - Read `.specify/templates/phr-template.prompt.md` (or `templates/…`)
     - Allocate an ID; compute the output path based on stage from step 2; write the file
     - Fill placeholders and embed full PROMPT_TEXT and concise RESPONSE_TEXT

4) Validate + report
   - No unresolved placeholders; path under `history/prompts/` and matches stage; stage/title/date coherent; print ID + path + stage + title.
   - On failure: warn, don't block. Skip only for `/sp.phr`.

## Response snapshot

This plan integrates an AI Chatbot into the existing Todo App using OpenAI Agents SDK and MCP (Model Context Protocol). The implementation follows a stateless architecture where all conversation state is persisted in Neon PostgreSQL. The system exposes task operations (add, list, complete, update, delete) as MCP tools that the AI agent can use to manage user tasks through natural language. Sequential integer IDs are used for all tasks and conversations to ensure consistent referencing. The frontend integrates OpenAI ChatKit into the existing dashboard UI while maintaining security through the existing authentication system.

## Technical Context

**Language/Version**: Python 3.13+, TypeScript 5.5+
**Primary Dependencies**: FastAPI, SQLModel, OpenAI Agents SDK, Official MCP SDK, Next.js 16+, Tailwind CSS
**Storage**: Neon Serverless PostgreSQL via SQLModel ORM
**Testing**: pytest for backend, Jest/React Testing Library for frontend
**Target Platform**: Linux server (backend), Web browser (frontend)
**Project Type**: Web application (backend + frontend)
**Performance Goals**: <200ms p95 response time for chat interactions, support 1000+ concurrent users
**Constraints**: Must be stateless server architecture, all state persisted in DB, sequential integer IDs for tasks/conversations
**Scale/Scope**: Individual user conversations, multi-tenant with user isolation

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Compliance Verification:
- ✅ **Statelessness**: Server must be stateless with all state persisted in database (FR-009)
- ✅ **Sequential Integer IDs**: Tasks and conversations must use sequential integer IDs (FR-002)
- ✅ **Security**: AI chatbot must be protected by existing auth system (FR-006)
- ✅ **MCP Integration**: Task operations must be exposed through MCP tools (FR-008)
- ✅ **No Breaking Changes**: Existing Phase 2 Auth/Task logic must remain intact
- ✅ **OpenAI Agents SDK**: Must use OpenAI Agents SDK as mandated
- ✅ **Database Extensions**: Need Conversation and Message models in existing SQLModel
- ✅ **Frontend Integration**: Must integrate OpenAI ChatKit with existing dashboard theme

## Project Structure

### Documentation (this feature)

```text
specs/001-ai-chatbot-integration/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

backend/
├── src/
│   ├── models.py            # Extended with Conversation and Message models
│   ├── mcp/
│   │   └── server.py        # MCP tools implementation for task operations
│   ├── agent/
│   │   └── runner.py        # OpenAI Agent logic and conversation handling
│   ├── routers/
│   │   ├── chat.py          # Chat API endpoint
│   │   └── tasks.py         # Existing task operations (unchanged)
│   ├── database.py          # Database connection and session management
│   └── main.py              # FastAPI app with MCP integration
└── tests/
    ├── unit/
    ├── integration/
    └── contract/

frontend/
├── src/
│   ├── app/
│   │   └── dashboard/
│   │       └── page.tsx     # Main dashboard with integrated chat
│   ├── components/
│   │   └── chat/
│   │       └── ChatInterface.tsx  # OpenAI ChatKit integration
│   └── services/
│       └── api.ts           # API client for chat endpoint
└── tests/

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None      | None       | All requirements compliant          |

## Summary

This plan integrates an AI Chatbot into the existing Todo App using OpenAI Agents SDK and MCP (Model Context Protocol). The implementation follows a stateless architecture where all conversation state is persisted in Neon PostgreSQL. The system exposes task operations (add, list, complete, update, delete) as MCP tools that the AI agent can use to manage user tasks through natural language. Sequential integer IDs are used for all tasks and conversations to ensure consistent referencing. The frontend integrates OpenAI ChatKit into the existing dashboard UI while maintaining security through the existing authentication system.

## Outcome

- ✅ Impact: Complete implementation plan created with research, data models, contracts, and quickstart guide
- 🧪 Tests: All constitution checks passed for compliance
- 📁 Files: Created plan.md, research.md, data-model.md, contracts/chat-api.yaml, quickstart.md
- 🔁 Next prompts: Ready for /sp.tasks to generate implementation tasks
- 🧠 Reflection: Planning phase completed successfully with all required artifacts

## Evaluation notes (flywheel)

- Failure modes observed: None - all planning steps completed successfully
- Graders run and results (PASS/FAIL): PASS - all constitution compliance checks passed
- Prompt variant (if applicable): Standard /sp.plan workflow
- Next experiment (smallest change to try): Generate tasks with /sp.tasks command
