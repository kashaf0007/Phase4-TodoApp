# Phase II Full-Stack Todo Application

A production-ready, multi-user todo application with JWT-based authentication and strict user isolation.

## Features

- ✅ User registration and authentication
- ✅ Create tasks with title and description
- ✅ View task list (newest first)
- ✅ Mark tasks as complete/incomplete
- ✅ Edit task details
- ✅ Delete tasks with confirmation
- ✅ Session persistence (7 days)
- ✅ Strict user isolation
- ✅ Responsive design

## Quick Start

See `specs/001-fullstack-todo-app/quickstart.md` for detailed setup instructions.

### Prerequisites
- Python 3.11+
- Node.js 18+
- Neon PostgreSQL account

### Setup
1. Generate JWT secret: `openssl rand -base64 32`
2. Configure `.env` files with BETTER_AUTH_SECRET and DATABASE_URL
3. Run backend: `cd backend && pip install -r requirements.txt && uvicorn src.main:app --reload`
4. Run frontend: `cd frontend && npm install && npm run dev`
5. Visit: http://localhost:3000

## Production Deployment

### Backend (Hugging Face Space)
Deploy the backend to Hugging Face Spaces:
1. Create a Hugging Face Space with the backend code
2. Configure environment variables:
   - `BETTER_AUTH_SECRET`: Your JWT secret
   - `DATABASE_URL`: Your Neon PostgreSQL connection string
3. The backend will be accessible at: `https://your-username-todo-phase02.hf.space`

### Frontend (Vercel)
Deploy the frontend on Vercel:
1. Push your code to a GitHub repository
2. Connect your repository to Vercel
3. In the Vercel dashboard, set the following environment variables:
   - `NEXT_PUBLIC_API_URL`: Your Hugging Face backend URL (e.g., `https://kashafaman123-todo-phase02.hf.space`)
   - `BETTER_AUTH_SECRET`: The same JWT secret used in your backend
4. Set the build command to: `cd frontend && npm install && npm run build`
5. Set the output directory to: `frontend/.next`

## Kubernetes Deployment (Phase IV)

Deploy the application to a local Kubernetes cluster using Helm charts.

### Prerequisites for Kubernetes Deployment
- Minikube (v1.20 or higher)
- kubectl
- Helm (v3.0 or higher)
- Docker

### Kubernetes Setup
1. Start Minikube with ingress addon:
   ```bash
   minikube start --addons=ingress
   ```

2. Create the dedicated namespace:
   ```bash
   kubectl create namespace todo-namespace
   ```

3. Build and load container images into Minikube (assuming you have Dockerfiles for frontend and backend):
   ```bash
   # Build frontend image
   docker build -f Dockerfile.frontend -t todo-app:frontend-v1.0 .
   minikube image load todo-app:frontend-v1.0

   # Build backend image
   docker build -f Dockerfile.backend -t todo-app:backend-v1.0 .
   minikube image load todo-app:backend-v1.0
   ```

### Kubernetes Deployment
Deploy the application using Helm:

```bash
helm upgrade --install todo-chatbot ./charts/todo-chatbot \
  --namespace todo-namespace \
  --set frontend.image.tag=frontend-v1.0 \
  --set backend.image.tag=backend-v1.0
```

### Accessing the Application in Kubernetes
1. Get the Minikube IP:
   ```bash
   minikube ip
   ```

2. Access the frontend at `http://[MINIKUBE_IP]` and the API at `http://[MINIKUBE_IP]/api`

### Kubernetes Validation
Run the following commands to verify the deployment:

```bash
# Check all pods are running
kubectl get pods -n todo-namespace

# Check all services are properly configured
kubectl get services -n todo-namespace

# Check ingress rules are active
kubectl get ingress -n todo-namespace
```

### Kubernetes Cleanup
To remove the deployment:

```bash
helm uninstall todo-chatbot -n todo-namespace
kubectl delete namespace todo-namespace
```

### Kubernetes Troubleshooting

#### Common Issues

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

### Important Notes
- Both frontend and backend must use the same `BETTER_AUTH_SECRET`
- The backend is configured to allow CORS requests from `https://hackathon2-phase1-five.vercel.app`
- Make sure both services are deployed and running before testing

## Documentation
- Specification: `specs/001-fullstack-todo-app/spec.md`
- Implementation Plan: `specs/001-fullstack-todo-app/plan.md`
- API Contract: `specs/001-fullstack-todo-app/contracts/api-spec.yaml`
- Quickstart Guide: `specs/001-fullstack-todo-app/quickstart.md`
