


<!--
Sync Impact Report:
- Version: 1.0.0 → 2.0.0 (Major update - transitioning from Phase II to Phase III)
- Principles Removed: 14 Phase II principles retired
- Principles Added: 14 new Phase III principles established
- Sections Added: Preamble, Purpose & Objectives, Architectural Constitution, Data Sovereignty & Models,
  MCP Tool Constitution, Agent Behavioral Law, Stateless Conversation Flow Law, Security & Authentication,
  Development Process Law, Deliverables Mandate, Amendments clause
- Sections Removed: Technology Stack (immutable), REST API Contract, Authentication & Security Constitution,
  Monorepo Constitution, Database Rules, Validation & Acceptance Criteria, Enforcement Clause
- Templates Status:
  ✅ plan-template.md - Constitution Check section aligns with new agentic workflow
  ✅ spec-template.md - User stories and requirements align with AI chatbot objective
  ✅ tasks-template.md - Task structure aligns with agentic implementation principle
- Follow-up: Update dependent artifacts to reflect new Phase III scope
-->

# 📜 Constitution of the Phase III Todo AI Chatbot Project

## 1. Preamble

We, the builders of the **Phase III Todo AI Chatbot**, establish this Constitution to define the guiding principles, architectural laws, behavioral rules, and technological boundaries governing the design, development, and evaluation of this system. This document ensures consistency, fairness, scalability, and transparency throughout the project lifecycle and serves as the single source of truth for reviewers, developers, and AI agents involved.

This project is evaluated not only on functionality, but on **architectural correctness, agentic workflow discipline, and strict adherence to stateless, tool-driven AI design**.

---

## 2. Purpose & Objectives

### 2.1 Core Objective

To build an **AI-powered, natural-language Todo management chatbot** that:

* Uses **Model Context Protocol (MCP)** tools for all task operations
* Operates through a **stateless backend architecture**
* Persists all state in a **Neon Serverless PostgreSQL database**
* Is driven entirely by **OpenAI Agents SDK** decision-making

### 2.2 Evaluation Objective

This project demonstrates:

* Proper use of **Agentic Dev Stack workflow**
* Correct separation of concerns between UI, Agent, Tools, and Storage
* Zero manual coding outside AI-assisted generation (Claude Code)

---

## 3. Foundational Principles (Articles)

### Article I — Agentic Authority

* All business logic decisions **must be made by an AI Agent**.
* The backend **must not** contain hard-coded intent detection or rule-based routing.
* The Agent selects and invokes MCP tools autonomously.

### Article II — Tool-Only Side Effects

* **All state-changing actions** (create, update, delete, complete tasks) **must occur exclusively via MCP tools**.
* The Agent **cannot** directly manipulate the database.
* MCP tools act as the **only bridge** between AI reasoning and persistence.

### Article III — Statelessness

* The FastAPI server **shall remain stateless**.
* No in-memory session storage, global variables, or cached conversation state is permitted.
* Every request must be independently reproducible using database state alone.

### Article IV — Persistent Memory

* Conversation context **must be reconstructed** on each request using database records.
* All user and assistant messages **must be stored** before and after agent execution.

---

## 4. Architectural Constitution

### 4.1 System Components

| Layer                 | Responsibility                           |
| --------------------- | ---------------------------------------- |
| ChatKit UI            | User interaction & message display       |
| FastAPI Chat Endpoint | Stateless orchestration layer            |
| OpenAI Agents SDK     | Reasoning, planning, and tool selection  |
| MCP Server            | Execution of task-related tools          |
| Neon PostgreSQL       | Persistent state and conversation memory |

### 4.2 Single Entry Point Law

* The system exposes **one primary conversational endpoint**:

  * `POST /api/{user_id}/chat`
* All user intentions flow through this endpoint.

---

## 5. Data Sovereignty & Models

### 5.1 Database Authority

* **Neon Serverless PostgreSQL** is the sole persistence layer.
* No alternative databases, caches, or file storage are permitted.

### 5.2 Canonical Data Models

#### Task

* user_id
* id
* title
* description
* completed
* created_at
* updated_at

#### Conversation

* user_id
* id
* created_at
* updated_at

#### Message

* user_id
* id
* conversation_id
* role (user | assistant)
* content
* created_at

All models are implemented using **SQLModel ORM**.

---

## 6. MCP Tool Constitution

### 6.1 Mandatory Tool Set

The MCP Server **must expose exactly the following tools**:

1. add_task
2. list_tasks
3. complete_task
4. delete_task
5. update_task

### 6.2 Tool Purity Rule

* MCP tools:

  * Are stateless
  * Accept explicit parameters
  * Perform a single responsibility
  * Return structured, deterministic output

### 6.3 Tool Invocation Transparency

* Every tool invocation **must be logged** and returned in the API response under `tool_calls`.

---

## 7. Agent Behavioral Law

### 7.1 Intent-to-Tool Mapping

The Agent **must follow these behavioral guarantees**:

| User Intent     | Required Action |
| --------------- | --------------- |
| Add / remember  | add_task        |
| Show / list     | list_tasks      |
| Complete / done | complete_task   |
| Delete / remove | delete_task     |
| Update / change | update_task     |

### 7.2 Multi-Step Reasoning

* When ambiguity exists (e.g., "delete the meeting task"), the Agent **must chain tools**:

  1. list_tasks
  2. delete_task

### 7.3 Confirmation Mandate

* Every successful mutation **must be confirmed** with a friendly natural-language response.

### 7.4 Error Dignity Clause

* Errors (task not found, invalid input) must be:

  * Gracefully explained
  * Non-technical
  * Action-guiding

---

## 8. Stateless Conversation Flow Law

Each request **must strictly follow this order**:

1. Receive user message
2. Fetch conversation history from database
3. Build agent input (history + new message)
4. Persist user message
5. Execute Agent with MCP tools
6. Persist assistant response
7. Return response

Deviation from this order constitutes a constitutional violation.

---

## 9. Security & Authentication

### 9.1 Authentication Authority

* **Better Auth** governs user identity.
* `user_id` is mandatory for all operations.

### 9.2 Frontend Domain Security

* Hosted ChatKit **must use OpenAI Domain Allowlist**.
* Domain keys are required in production environments.

---

## 10. Development Process Law

### 10.1 Agentic Dev Stack Compliance

All development **must follow this sequence**:

1. Write specification
2. Generate implementation plan
3. Break plan into tasks
4. Implement via Claude Code

Manual coding outside AI assistance is **strictly prohibited**.

### 10.2 Reviewability Clause

* Prompts, iterations, and generated artifacts **must remain reviewable**.

---

## 11. Deliverables Mandate

The final submission **must include**:

* Functional chatbot
* GitHub repository
* Frontend, backend, specs directories
* Database migrations
* Setup & deployment README

---

## 12. Amendments

This Constitution may be amended **only if**:

* Core principles (statelessness, MCP-only mutations, agent authority) remain intact
* Amendments are documented and justified

---

## 13. Ratification

This Constitution is hereby adopted as the **supreme governing document** of the Phase III Todo AI Chatbot project.

Any implementation that violates these articles shall be considered **architecturally invalid**, regardless of functional correctness.

---

**📌 End of Constitution**

**Version**: 2.0.0 | **Ratified**: 2025-12-30 | **Last Amended**: 2026-01-23

