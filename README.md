# Travel Planner App - DevOps Portfolio Project

A full-stack travel planning product and DevOps portfolio project. Roam combines a polished Next.js experience with Python services, machine-learning recommendations, GitHub Actions, GitOps, and MLOps.

## Product Experience

The user-facing application lives in `web/` and provides:

- A responsive trip-planning workspace
- Destination inspiration
- Travel mood, dates, and budget inputs
- Generated itinerary previews
- Demo mode while backend services are unavailable

The product roadmap is documented in [PRODUCT_BUILD_PLAN.md](PRODUCT_BUILD_PLAN.md).

## Architecture Overview

### Services
- **Roam Web**: Next.js and TypeScript travel-planning interface
- **Recommendation Engine**: ML-powered destination recommendations
- **User API**: User profile and preference management
- **Trip Planner**: Itinerary and cost planning

### DevOps & Infrastructure
- **Docker**: Containerized frontend and backend services
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
- Node.js 20+

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

### 4. Run the web application
```bash
cd web
npm install
npm run dev
```

Open http://localhost:3000 for the Roam product experience. The frontend runs in demo mode unless `NEXT_PUBLIC_TRIP_PLANNER_URL` is configured. Copy `web/.env.example` to `web/.env.local` when connecting it to the Trip Planner API.

### 5. Access backend services
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

3. **Deployment validation** (`.github/workflows/deploy.yml`)
   - Lints the Helm chart
   - Renders the Kubernetes manifests
   - Verifies that generated output is non-empty

GitHub Actions publishes immutable images to public GHCR. Argo CD performs deployment from Git in the Kubernetes environment; it is intentionally not called directly by GitHub-hosted runners.

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
├── web/                        # Next.js product frontend
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

## Product And Platform Roadmap

1. Connect the Roam frontend to the Trip Planner API
2. Replace in-memory storage with PostgreSQL persistence
3. Add authentication and saved itineraries
4. Choose a hosting model and public ingress
5. Add production observability and model quality gates

## Development

See individual service README files in `/services/` for detailed development instructions.

## License

MIT
