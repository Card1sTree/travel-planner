# Travel Planner App - DevOps Portfolio Project

A production-ready travel recommendation and planning application showcasing modern DevOps practices with ArgoCD, GitHub Actions, GitOps, and MLOps.

## Architecture Overview

### Services
- **Recommendation Engine**: ML-powered destination recommendations
- **User API**: User profile and preference management
- **Trip Planner**: Itinerary and cost planning

### DevOps & Infrastructure
- **Kubernetes**: Container orchestration (Helm charts)
- **ArgoCD**: GitOps-based deployment management
- **GitHub Actions**: CI/CD pipelines
- **DVC**: Model and data versioning
- **PostgreSQL**: Data persistence

## Prerequisites

- Docker & Docker Compose
- Kubernetes (minikube/kind) or cloud cluster
- ArgoCD installed in K8s cluster
- GitHub Actions enabled
- Python 3.10+

## Quick Start - Local Development

### 1. Set up Python environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. Install dependencies
```bash
pip install -r ml/requirements.txt
pip install -r services/recommendation-engine/requirements.txt
```

### 3. Run with Docker Compose
```bash
docker-compose up -d
```

### 4. Access services
- Recommendation Engine: http://localhost:8001/docs
- User API: http://localhost:8002/docs
- Trip Planner: http://localhost:8003/docs

## CI/CD Workflow

### GitHub Actions Pipelines

1. **CI Pipeline** (`.github/workflows/ci.yml`)
   - Runs on every push
   - Tests all services
   - Builds Docker images
   - Pushes to registry

2. **Model Training** (`.github/workflows/train-model.yml`)
   - Scheduled daily or on-demand
   - Trains ML model
   - Versions model with DVC
   - Pushes changes to Git

3. **Deploy** (`.github/workflows/deploy.yml`)
   - ArgoCD syncs automatically
   - Updates Kubernetes deployments
   - Monitors rollout status

## GitOps with ArgoCD

All infrastructure and deployment configs are in Git. ArgoCD watches the repo and automatically syncs:

```bash
# Apply ArgoCD Application
kubectl apply -f deployment-chart/argocd/application.yaml
```

View in ArgoCD UI:
```bash
kubectl port-forward -n argocd svc/argocd-server 8080:443
```

## MLOps Pipeline

### Model Training & Versioning

```bash
# Install DVC
pip install dvc

# Track datasets and models
dvc add ml/data/travel_data.csv
dvc add ml/models/recommendation_model.pkl

# Train model
python ml/train.py
```

Models are versioned and tracked in Git via DVC.

## Project Structure

```
.
├── .github/workflows/          # GitHub Actions CI/CD
├── ml/                         # ML training pipeline
├── services/                   # Microservices
│   ├── recommendation-engine/
│   ├── user-api/
│   └── trip-planner/
├── deployment-chart/           # Kubernetes manifests & Helm
│   ├── templates/
│   └── argocd/
├── docker-compose.yml          # Local development
└── dvc.yaml                    # DVC pipeline configuration
```

## Key Features Demonstrated

✅ **GitOps**: All infrastructure in Git, ArgoCD keeps cluster in sync  
✅ **CI/CD**: GitHub Actions automates testing, building, and deployment  
✅ **MLOps**: Model training, versioning, and continuous retraining  
✅ **Microservices**: Multiple services with Kubernetes orchestration  
✅ **IaC**: Helm charts for reproducible infrastructure  
✅ **Monitoring**: Ready for Prometheus/Grafana integration  

## Next Steps

1. Set up Kubernetes cluster (minikube/kind)
2. Install ArgoCD
3. Configure Docker registry credentials
4. Set up GitHub repository secrets
5. Deploy initial Helm release

## Development

See individual service README files in `/services/` for detailed development instructions.

## License

MIT
