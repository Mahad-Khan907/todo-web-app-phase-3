<!--
SYNC IMPACT REPORT:
- Version change: 1.2.0 → 1.3.0
- Modified sections: Project Overview, Technical Stack, Phase III Specific Rules, Project Structure
- Added sections: Database Extensions, Implementation Workflow
- Templates requiring updates: ✅ plan-template.md, ✅ spec-template.md, ✅ tasks-template.md
- Follow-up TODOs: None
-->

# Project Constitution: Todo AI Chatbot (Phase 3)

## Project Overview

### Project Mission
This project is an evolution of a Todo Web App. Phase 2 (Infrastructure & Auth) is COMPLETE. Phase 3 focuses on building a Stateless AI Chatbot using MCP (Model Context Protocol) and OpenAI Agents SDK, integrated into the existing monorepo.

## Technical Stack (Phase 3 Integration)

### Backend (API Layer)
- **Runtime**: Python 3.13+
- **Management**: `uv` (Mandatory for environments and dependencies)
- **Framework**: FastAPI (High-performance REST API)
- **AI Logic**: OpenAI Agents SDK + Official MCP SDK
- **MCP Server**: Integrated into FastAPI to expose Task operations as tools
- **Database**: Neon Serverless PostgreSQL (SQLModel ORM)
- **Auth**: JWT-based security using `python-jose` - AI must be protected by existing auth

### Frontend (UI Layer)
- **Framework**: Next.js 16+ (App Router)
- **Language**: TypeScript (Strict typing)
- **Styling**: Tailwind CSS (Premium Dark Theme) + Shadcn/UI
- **State**: TanStack Query (Server-state management)
- **Auth**: Better Auth integration
- **AI Interface**: OpenAI ChatKit integrated into the existing Dashboard theme

## Phase 3 Core Rules

### 1. Directory Structure
- New specifications must be stored in `specs/003-ai-chatbot/`.
- Backend logic stays in `backend/src/` (new modules: `mcp_server.py`, `agent_logic.py`).
- Frontend chat interface must match the existing Dashboard's theme/styling.

### 2. Statelessness
- The `/api/chat` endpoint and MCP tools MUST be stateless.
- All state (conversations/messages) must be persisted in the database.

### 3. Sub-Agent Usage
- Claude Code (the sub-agent) MUST be used for all file modifications and terminal commands.

### 4. No Breaking Changes
- Do not modify existing Phase 2 Auth or Task CRUD logic unless necessary for MCP tool integration.
- Reuse existing SQLModel models where possible.

### 5. Security
- The AI Chatbot is only accessible to logged-in users.
- The `user_id` must be extracted from the existing auth dependency.

## Database Extensions

Phase 3 requires new models in `backend/src/models.py`:
- `Conversation`: `id`, `user_id`, `created_at`, `updated_at`
- `Message`: `id`, `conversation_id`, `user_id`, `role` (user/assistant), `content`, `created_at`

## Implementation Workflow (Spec-Driven)

### 1. Specify
Create `/specs/003-ai-chatbot/spec.md` for AI behavior and MCP tools.

### 2. Plan
Generate `/specs/003-ai-chatbot/plan.md` for implementation roadmap.

## Operational Rules & "No Error" Policy

### Development Standards
- **Clean Architecture**: Strictly separate logic into `/backend` and `/frontend`.
- **Dependency Isolation**: All backend libraries must be managed via `uv`. Never use global pip.
- **Validation**: Every feature must pass a `/sp.specify` check before implementation to ensure no logical gaps.
- **Error-Free Code**: Claude must verify syntax, TypeScript types, and import paths before delivering code snippets to prevent build breaks.
- **AI Integration**: All new features must be compatible with AI natural language processing via MCP tools and OpenAI Agents.

### CLI Commands
- `/sp.constitution`: Update project rules.
- `/sp.specify`: Generate or refine feature requirements.
- `/sp.plan`: Create a technical roadmap.
- `/sp.tasks`: Generate a granular checklist for implementation.
- `/sp.implement`: Execute code generation based on tasks.
- `/sp.adr`: Document architecturally significant decisions.
- `/sp.analyze`: Perform cross-artifact consistency analysis.

## Governance
All development must strictly adhere to this constitution to ensure alignment with project requirements. Constitution supersedes all other practices. All code generation must follow spec-driven development principles using Claude Code and Spec-Kit Plus tools. All PRs/reviews must verify compliance with these principles. AI-native features must leverage MCP tools and OpenAI Agents SDK as mandated by the Core Rules.

**Version**: 1.3.0 | **Ratified**: 2025-12-28 | **Last Amended**: 2026-01-06