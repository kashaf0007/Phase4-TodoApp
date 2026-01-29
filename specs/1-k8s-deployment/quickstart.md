# Quickstart Guide: Todo Chatbot Kubernetes Deployment

**Feature**: 1-k8s-deployment | **Date**: 2026-01-29

## Prerequisites

Before deploying the Todo Chatbot application to Kubernetes, ensure you have the following tools installed:

- **Minikube**: Local Kubernetes cluster (v1.20 or higher)
- **kubectl**: Kubernetes command-line tool (matching Minikube version)
- **Helm**: Package manager for Kubernetes (v3.0 or higher)
- **Docker**: Container runtime (required for Gordon AI)

Verify your setup with these commands:

```bash
minikube version
kubectl version --client
helm version
docker --version
```

## Environment Setup

### 1. Start Minikube Cluster

Initialize your local Kubernetes cluster with the NGINX Ingress addon:

```bash
minikube start --addons=ingress
```

Verify the cluster is running:

```bash
kubectl cluster-info
kubectl get nodes
```

### 2. Enable Required Addons

Ensure the NGINX ingress controller is running:

```bash
minikube addons list | grep ingress
```

If disabled, enable it:

```bash
minikube addons enable ingress
```

## Deployment Steps

### 1. Containerization (Using Gordon AI)

Generate optimized Dockerfiles for frontend and backend:

```bash
# Generate Dockerfile for frontend
gordon generate --context ./frontend --output Dockerfile.frontend

# Generate Dockerfile for backend
gordon generate --context ./backend --output Dockerfile.backend
```

Build and load images directly into Minikube:

```bash
# Build frontend image
docker build -f Dockerfile.frontend -t todo-app:frontend-v1.0 .
minikube image load todo-app:frontend-v1.0

# Build backend image
docker build -f Dockerfile.backend -t todo-app:backend-v1.0 .
minikube image load todo-app:backend-v1.0
```

### 2. Helm Chart Generation (Using kubectl-ai)

Generate the Helm chart structure:

```bash
kubectl-ai "generate helm chart todo-chatbot with frontend, backend, and postgresql deployments"
```

Customize the generated chart with the required specifications:

```bash
kubectl-ai "update todo-chatbot chart to set frontend replicas to 2"
kubectl-ai "update todo-chatbot chart to set backend replicas to 2"
kubectl-ai "update todo-chatbot chart to use postgresql StatefulSet with 1Gi PVC"
```

### 3. Namespace and Configuration Setup

Create the dedicated namespace:

```bash
kubectl create namespace todo-namespace
```

Apply configuration and secrets:

```bash
kubectl-ai "create ConfigMap todo-config in namespace todo-namespace with API_URL=http://localhost:30001/api"
kubectl-ai "create Secret db-credentials in namespace todo-namespace with POSTGRES_USER=admin, POSTGRES_PASSWORD=secretpassword"
```

### 4. Deploy the Application

Install the Helm chart:

```bash
helm upgrade --install todo-chatbot ./charts/todo-chatbot \
  --namespace todo-namespace \
  --set frontend.image.tag=frontend-v1.0 \
  --set backend.image.tag=backend-v1.0
```

### 5. Configure Ingress

Create ingress rules for path-based routing:

```bash
kubectl-ai "create ingress todo-ingress in namespace todo-namespace that routes / to frontend-service and /api to backend-service"
```

## Verification Steps

### 1. Check Pod Status

Verify all pods are running:

```bash
kubectl get pods -n todo-namespace
```

Expected output should show all pods in "Running" status.

### 2. Check Services

Verify services are properly configured:

```bash
kubectl get services -n todo-namespace
```

### 3. Check Ingress

Verify ingress rules are active:

```bash
kubectl get ingress -n todo-namespace
```

### 4. Access the Application

Get the Minikube IP:

```bash
minikube ip
```

Access the frontend at `http://[MINIKUBE_IP]` and the API at `http://[MINIKUBE_IP]/api`.

## Validation (Using Kagent)

Run the final validation:

```bash
kagent "Check the health of todo-namespace and verify if the frontend can reach the backend."
```

## Troubleshooting

### Common Issues

1. **Images not found**: Ensure images are loaded into Minikube:
   ```bash
   minikube image ls | grep todo-app
   ```

2. **Ingress not working**: Check if NGINX ingress controller is running:
   ```bash
   kubectl get pods -n ingress-nginx
   ```

3. **Pods in CrashLoopBackOff**: Check pod logs:
   ```bash
   kubectl logs -n todo-namespace [POD_NAME]
   ```

### Cleanup

To remove the deployment:

```bash
helm uninstall todo-chatbot -n todo-namespace
kubectl delete namespace todo-namespace
```

## Next Steps

- Configure persistent storage for production use
- Set up monitoring and logging
- Implement CI/CD pipeline
- Configure TLS/SSL certificates