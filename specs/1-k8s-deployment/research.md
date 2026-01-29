# Research: Kubernetes Deployment for Todo Chatbot

**Feature**: 1-k8s-deployment | **Date**: 2026-01-29

## Executive Summary

This research document outlines the technical decisions and approaches for deploying the Todo Chatbot application to a local Minikube Kubernetes cluster. The implementation will follow the agentic workflow using Gordon for containerization, kubectl-ai for manifest generation, and Kagent for validation.

## Technology Stack Analysis

### Container Runtime & Orchestration
**Decision**: Use Docker for containerization and Kubernetes for orchestration via Minikube
**Rationale**: Kubernetes is the industry standard for container orchestration, providing scaling, resilience, and service discovery. Minikube offers a local development environment that closely mirrors production.

**Alternatives considered**:
- Docker Compose: Simpler but lacks advanced orchestration features
- Podman + Kubernetes: Good alternative but Docker is more widely adopted
- Cloud deployment: Would require cloud accounts and costs

### Base Images for Multi-stage Builds
**Decision**: Use Alpine Linux as base for production images
**Rationale**: Alpine provides minimal footprint, reduced attack surface, and faster downloads. It's well-established for production container images.

**Alternatives considered**:
- Ubuntu slim: Larger but more familiar for debugging
- Debian slim: Balance between size and compatibility
- Distroless: Minimal but harder to troubleshoot

### Ingress Controller Selection
**Decision**: Use NGINX Ingress Controller
**Rationale**: NGINX is mature, well-documented, and widely adopted in the Kubernetes ecosystem. It supports the path-based routing required for this application.

**Alternatives considered**:
- Traefik: Modern alternative with good features but slightly more complex
- Kong: Feature-rich but overkill for this use case
- AWS ALB: Only applicable for cloud deployments

## Kubernetes Resource Decisions

### Stateful vs Stateless Workloads
**Decision**:
- Frontend and backend as Deployments (stateless)
- Database as StatefulSet (stateful)
**Rationale**: Frontend and backend can be replaced without data loss, while the database requires persistent storage and ordered deployment characteristics that StatefulSet provides.

**Alternatives considered**:
- Using Deployments for all: Would lose data on pod restarts
- Using StatefulSets for all: Unnecessary complexity for stateless services

### Service Discovery Pattern
**Decision**: Use ClusterIP services for internal communication and NodePort for external access
**Rationale**: ClusterIP provides stable internal DNS names for service-to-service communication. NodePort enables external access in the local Minikube environment.

**Alternatives considered**:
- Headless services: Would complicate DNS resolution
- LoadBalancer: Requires cloud provider integration
- ExternalIPs: Less portable across environments

### Storage Solution
**Decision**: Use PersistentVolumeClaim with hostPath storage in Minikube
**Rationale**: PVC provides abstraction over underlying storage while ensuring data persistence across pod restarts. HostPath is appropriate for local development.

**Alternatives considered**:
- EmptyDir: Would lose data on pod restarts
- Cloud storage: Not applicable for local Minikube
- Local volumes: More complex setup for local environment

## Security Considerations

### Container Security
**Decision**: Run containers as non-root users where possible
**Rationale**: Reduces potential damage from security vulnerabilities by limiting privileges within the container.

**Alternatives considered**:
- Root user: Simpler but increases security risk
- Specific UID ranges: More complex but potentially more secure

### Secret Management
**Decision**: Use Kubernetes native Secrets for sensitive data
**Rationale**: Kubernetes Secrets provide encryption at rest and access control. They integrate well with the platform.

**Alternatives considered**:
- Environment variables in ConfigMaps: Exposes secrets in plain text
- External secret stores: Overkill for local development
- Mounted files: Adds complexity without significant benefit

## Resource Management

### Resource Requests and Limits
**Decision**: Set CPU requests at 100m/200m limits and memory at 128Mi/256Mi as specified
**Rationale**: These values provide adequate resources for the application while preventing resource exhaustion. The 2:1 ratio between limits and requests allows for burst capacity.

**Alternatives considered**:
- Higher values: Would consume more cluster resources
- No limits: Could lead to resource contention
- Lower values: Might cause performance issues or OOM kills

## Monitoring and Health Checks

### Health Probes Implementation
**Decision**: Implement both liveness and readiness probes
**Rationale**: Readiness probes ensure traffic is only sent to healthy instances. Liveness probes restart unhealthy pods automatically, improving resilience.

**Alternatives considered**:
- No health checks: Would reduce resilience
- Only readiness probes: Would not automatically recover from stuck states
- Custom health endpoints: Would require application changes

## Agentic Workflow Integration

### Tool Selection Justification
**Decision**: Use Gordon for Dockerfiles, kubectl-ai for manifests, Kagent for validation
**Rationale**: These tools align with the constitutional requirements and provide AI-powered generation of infrastructure code.

**Alternatives considered**:
- Manual creation: Violates constitutional requirements
- Other AI tools: Would require different skill sets
- Template-based generators: Less flexible than AI tools