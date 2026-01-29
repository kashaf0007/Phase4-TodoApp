---
description: "Task list for Kubernetes deployment of Todo Chatbot"
---

# Tasks: Kubernetes Deployment

**Input**: Design documents from `/specs/1-k8s-deployment/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Verify Minikube, kubectl, Helm, and Docker are installed and accessible
- [X] T002 [P] Create directory structure: `charts/todo-chatbot/templates/` and `infrastructure/`
- [X] T003 [P] Initialize Helm chart with `helm create todo-chatbot` in charts directory

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [X] T004 Start Minikube cluster with ingress addon enabled: `minikube start --addons=ingress`
- [X] T005 [P] Create dedicated namespace: `kubectl create namespace todo-namespace`
- [X] T006 [P] Generate Dockerfiles for frontend and backend using Gordon AI
- [X] T007 Build and load container images into Minikube: `minikube image load todo-app:frontend-v1.0` and `minikube image load todo-app:backend-v1.0`
- [X] T008 Create ConfigMap and Secret resources for application configuration

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Deploy Infrastructure (Priority: P1) 🎯 MVP

**Goal**: Deploy the Todo Chatbot application to a local Kubernetes cluster with scaling and resilience capabilities

**Independent Test**: Can be fully tested by verifying all pods are running and services are accessible in the Minikube cluster

### Implementation for User Story 1

- [X] T009 [P] [US1] Create PostgreSQL StatefulSet with 1 replica in charts/todo-chatbot/templates/postgres-statefulset.yaml
- [X] T010 [P] [US1] Create PostgreSQL Service in charts/todo-chatbot/templates/postgres-service.yaml
- [X] T011 [P] [US1] Create PersistentVolumeClaim for database in charts/todo-chatbot/templates/postgres-pvc.yaml
- [X] T012 [US1] Create Backend Deployment with 2 replicas in charts/todo-chatbot/templates/backend-deployment.yaml
- [X] T013 [US1] Create Backend Service in charts/todo-chatbot/templates/backend-service.yaml
- [X] T014 [US1] Create Frontend Deployment with 2 replicas in charts/todo-chatbot/templates/frontend-deployment.yaml
- [X] T015 [US1] Create Frontend Service with NodePort 30001 in charts/todo-chatbot/templates/frontend-service.yaml
- [X] T016 [US1] Add resource limits (CPU: 100m/200m, Memory: 128Mi/256Mi) to all deployments
- [X] T017 [US1] Add liveness and readiness probes to all deployments
- [X] T018 [US1] Update Helm values.yaml with image tags and configuration values

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Access Application (Priority: P2)

**Goal**: Enable access to the Todo Chatbot application via a stable URL with proper routing

**Independent Test**: Can be fully tested by accessing the frontend service and verifying the application loads correctly

### Implementation for User Story 2

- [X] T019 [P] [US2] Create Ingress resource for path-based routing in charts/todo-chatbot/templates/ingress.yaml
- [X] T020 [US2] Configure Ingress to route `/` to frontend-service and `/api` to backend-service
- [X] T021 [US2] Test application accessibility via Minikube IP address
- [X] T022 [US2] Verify API requests are properly routed from frontend to backend

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Data Persistence (Priority: P3)

**Goal**: Ensure todo data persists across application restarts without data loss

**Independent Test**: Can be fully tested by creating data, restarting pods, and verifying data remains intact

### Implementation for User Story 3

- [X] T023 [P] [US3] Configure PostgreSQL StatefulSet with proper volume mounts for persistent storage
- [X] T024 [US3] Test data persistence by creating todo items, restarting database pod, and verifying data remains
- [X] T025 [US3] Verify PVC maintains data across pod restarts and recreations

**Checkpoint**: All user stories should now be independently functional

---

[Add more user story phases as needed, following the same pattern]

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T026 [P] Update documentation in README.md with deployment instructions
- [X] T027 [P] Create validation script to run Kagent health checks
- [X] T028 Run quickstart.md validation steps to confirm complete functionality
- [X] T029 Clean up temporary files and optimize Docker images
- [X] T030 Document troubleshooting steps and common issues

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Different user stories can be worked on in parallel by different team members
- Tasks within each user story that are marked [P] can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all User Story 1 components together:
Task: "Create PostgreSQL StatefulSet with 1 replica in charts/todo-chatbot/templates/postgres-statefulset.yaml"
Task: "Create PostgreSQL Service in charts/todo-chatbot/templates/postgres-service.yaml"
Task: "Create PersistentVolumeClaim for database in charts/todo-chatbot/templates/postgres-pvc.yaml"
Task: "Create Backend Deployment with 2 replicas in charts/todo-chatbot/templates/backend-deployment.yaml"
Task: "Create Backend Service in charts/todo-chatbot/templates/backend-service.yaml"
Task: "Create Frontend Deployment with 2 replicas in charts/todo-chatbot/templates/frontend-deployment.yaml"
Task: "Create Frontend Service with NodePort 30001 in charts/todo-chatbot/templates/frontend-service.yaml"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence