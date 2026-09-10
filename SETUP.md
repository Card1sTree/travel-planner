# Quick Setup Guide

## Prerequisites
- Git
- Docker & Docker Compose
- kubectl (v1.24+)
- Helm (v3+)
- Python 3.10+

## 1. Local Development Setup

### Start all services locally
```bash
docker-compose up -d
```

### Access services
- Recommendation Engine API: http://localhost:8001/docs
- User API: http://localhost:8002/docs
- Trip Planner API: http://localhost:8003/docs
- PostgreSQL: localhost:5432

### Test the API
```bash
# Create a user
curl -X POST http://localhost:8002/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30,
    "budget": 3000,
    "preferred_activities": ["Beach", "Culture"]
  }'

# Get a recommendation
curl -X POST http://localhost:8001/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "age": 30,
    "budget": 3000,
    "travel_days": 7,
    "preferred_activity": "Beach",
    "travel_month": 6,
    "group_size": 2
  }'
```

## 2. Kubernetes Setup

### Prerequisites
Install a local Kubernetes cluster:
```bash
# Using minikube
minikube start --cpus=4 --memory=8192 --driver=docker

# Or using kind (Kubernetes in Docker)
kind create cluster --config kind-config.yaml
```

### Install ArgoCD
```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Wait for ArgoCD to be ready
kubectl wait --for=condition=available --timeout=300s \
  deployment/argocd-server -n argocd
```

### Access ArgoCD UI
```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
# Open https://localhost:8080 in browser
# Get password: kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath="{.data.password}" | base64 -d
```

### Create namespace
```bash
kubectl create namespace travel-app
```

## 3. GitHub Actions Setup

### Required Secrets
Add these to your GitHub repository settings → Secrets and variables:

1. **Docker Registry**
   - `DOCKER_USERNAME`: Your Docker Hub username
   - `DOCKER_PASSWORD`: Your Docker Hub token

2. **Kubernetes/ArgoCD**
   - `ARGOCD_SERVER`: Your ArgoCD server URL
   - `ARGOCD_TOKEN`: ArgoCD API token

3. **AWS (for DVC)**
   - `AWS_ACCESS_KEY_ID`: AWS credentials
   - `AWS_SECRET_ACCESS_KEY`: AWS credentials

4. **Notifications**
   - `SLACK_WEBHOOK`: Slack webhook URL (optional)

### Initial Setup Workflow
Run the setup workflow to initialize infrastructure:
1. Go to **Actions** → **Setup & Teardown**
2. Click **Run workflow**
3. Select **setup-argocd**
4. Select **setup-namespace**

## 4. MLOps - Model Training

### Manual Training
```bash
cd ml
python prepare_data.py
python train.py
python evaluate.py
```

### With DVC
```bash
# Initialize DVC
dvc init

# Run pipeline
dvc repro

# Track models
dvc add ml/models/recommendation_model.pkl
git add ml/models/recommendation_model.pkl.dvc
git commit -m "Updated model"
```

## 5. Deploy to Kubernetes

### Deploy using Helm
```bash
# Update image tags in deployment-chart/values.yaml first
helm install travel-planner deployment-chart/ \
  --namespace travel-app \
  --create-namespace

# Verify deployment
kubectl get all -n travel-app
```

### Deploy using ArgoCD
```bash
# Apply ArgoCD Application
kubectl apply -f deployment-chart/argocd/application.yaml

# Sync application
argocd app sync travel-app
```

### Access Services
```bash
# Get service IPs
kubectl get svc -n travel-app

# Port forward for testing
kubectl port-forward -n travel-app svc/trip-planner 8003:8000
```

## 6. Monitoring & Logging

### View logs
```bash
# All services
kubectl logs -n travel-app -f -l app=trip-planner

# Specific pod
kubectl logs -n travel-app <pod-name> -f
```

### Check deployment status
```bash
# Deployment status
kubectl rollout status deployment/trip-planner -n travel-app

# Pod details
kubectl describe pod -n travel-app <pod-name>
```

## DevOps Best Practices Demonstrated

✅ **GitOps**: All configs in Git, ArgoCD keeps cluster in sync  
✅ **CI/CD Automation**: GitHub Actions test, build, and deploy  
✅ **MLOps Pipeline**: Automated training, versioning with DVC  
✅ **Infrastructure as Code**: Helm charts, Kubernetes manifests  
✅ **Monitoring & Logging**: Health checks, service discovery  
✅ **Security**: Private registries, secret management  
✅ **Scalability**: Horizontal pod autoscaling, multi-replica services  
✅ **Reliability**: Liveness/readiness probes, deployment strategies  

## Troubleshooting

### Services not starting
```bash
kubectl logs -n travel-app <service-name>
kubectl describe pod -n travel-app <pod-name>
```

### ArgoCD not syncing
```bash
argocd app get travel-app
argocd app logs travel-app
```

### Database connection issues
```bash
kubectl port-forward -n travel-app svc/postgres 5432:5432
psql -U travel_user -d travel_db -h localhost
```

## Next Steps

1. Customize the Helm values for your environment
2. Set up monitoring with Prometheus & Grafana
3. Add security policies (NetworkPolicies, RBAC)
4. Implement GitOps secrets (sealed-secrets, external-secrets)
5. Set up automated testing for Kubernetes manifests
6. Configure backup strategy for databases
