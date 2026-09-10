# Travel App - MLOps & DevOps Showcase

Complete portfolio project demonstrating modern DevOps and MLOps practices.

## 🎯 Project Goals

**Showcase DevOps Expertise:**
- GitOps with ArgoCD
- CI/CD Automation with GitHub Actions
- Kubernetes Orchestration & Helm
- MLOps Pipeline with Model Versioning
- Infrastructure as Code
- Microservices Architecture

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│          GitHub Repository (Git)                │
│  - Source code, Kubernetes manifests, ML code   │
└──────────────────┬──────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
        v                     v
   ┌─────────────┐      ┌──────────────┐
   │GitHub       │      │GitHub        │
   │Actions:CI   │      │Actions:      │
   │- Test       │      │MLOps Train   │
   │- Build      │      │- DVC Pipeline│
   │- Push Image │      │- Metrics     │
   └─────────────┘      └──────────────┘
        │                     │
        └──────────┬──────────┘
                   │
        ┌──────────v──────────┐
        │  Docker Registry    │
        │  (Docker Hub)       │
        └──────────┬──────────┘
                   │
                   v
        ┌──────────────────────┐
        │   ArgoCD             │
        │   Watches Git Repo   │
        │   & Syncs K8s        │
        └──────────┬───────────┘
                   │
                   v
    ┌──────────────────────────────┐
    │  Kubernetes Cluster          │
    │ ┌──────────────────────────┐ │
    │ │ Recommendation Engine     │ │
    │ │ (RandomForest ML Model)   │ │
    │ ├──────────────────────────┤ │
    │ │ User API                 │ │
    │ │ (User Management)        │ │
    │ ├──────────────────────────┤ │
    │ │ Trip Planner             │ │
    │ │ (Orchestration)          │ │
    │ ├──────────────────────────┤ │
    │ │ PostgreSQL Database      │ │
    │ └──────────────────────────┘ │
    └──────────────────────────────┘
```

## 📋 Key Features

### DevOps Practices
- ✅ **GitOps**: All infrastructure configs in Git, ArgoCD auto-syncs
- ✅ **CI/CD**: GitHub Actions for testing, building, deploying
- ✅ **Infrastructure as Code**: Helm charts, Kubernetes manifests
- ✅ **Microservices**: 3 independent services with clear separation of concerns
- ✅ **Containerization**: Docker for all services
- ✅ **Orchestration**: Kubernetes with proper resource management
- ✅ **Service Discovery**: Kubernetes DNS
- ✅ **Load Balancing**: Kubernetes Services with auto-scaling

### MLOps Practices
- ✅ **Model Training Pipeline**: Automated DVC pipeline
- ✅ **Model Versioning**: Git-based with DVC
- ✅ **Experiment Tracking**: Metrics logging and comparison
- ✅ **Automated Retraining**: Scheduled GitHub Actions
- ✅ **Data Versioning**: DVC for datasets and models
- ✅ **Production Model Serving**: Containerized inference service

### Monitoring & Observability
- ✅ **Health Checks**: Liveness & readiness probes
- ✅ **Metrics**: Ready for Prometheus integration
- ✅ **Logging**: Structured logs with service context
- ✅ **Service Status**: Kubernetes dashboard integration

## 🚀 Quick Start

### 1. Local Development (Docker Compose)
```bash
# Start all services
docker-compose up -d

# Test services
curl http://localhost:8001/health  # Recommendation Engine
curl http://localhost:8002/health  # User API
curl http://localhost:8003/health  # Trip Planner
```

### 2. Kubernetes (Helm)
```bash
# Create namespace
kubectl create namespace travel-app

# Deploy with Helm
helm install travel-planner deployment-chart/ -n travel-app

# Check status
kubectl get all -n travel-app
```

### 3. GitOps with ArgoCD
```bash
# Install ArgoCD
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Deploy with ArgoCD
kubectl apply -f deployment-chart/argocd/application.yaml

# Access ArgoCD UI
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

## 📊 Workflows

### CI/CD Pipeline (.github/workflows/ci.yml)
1. **Trigger**: Push to main/develop
2. **Steps**:
   - Run tests
   - Build Docker images
   - Push to registry
   - Trigger ArgoCD sync
3. **Outcome**: Automatic deployment to Kubernetes

### MLOps Pipeline (.github/workflows/train-model.yml)
1. **Trigger**: Daily schedule or manual dispatch
2. **Steps**:
   - Prepare training data
   - Train Random Forest model
   - Evaluate model performance
   - Version model with DVC
   - Push changes to Git
3. **Outcome**: Updated model in registry

### Deployment (.github/workflows/deploy.yml)
1. **Trigger**: Kubernetes manifest changes
2. **Steps**:
   - Validate manifests
   - Trigger ArgoCD sync
   - Verify deployment health
   - Send notifications
3. **Outcome**: Rolling deployment with health checks

## 📁 Project Structure
```
travel-app/
├── .github/workflows/          # CI/CD, MLOps, Deployment automation
│   ├── ci.yml                 # Build & test pipeline
│   ├── train-model.yml        # ML training pipeline
│   ├── deploy.yml             # Kubernetes deployment
│   └── setup.yml              # Infrastructure setup
├── ml/                         # Machine Learning
│   ├── train.py               # Model training
│   ├── prepare_data.py        # Data preparation
│   ├── evaluate.py            # Model evaluation
│   ├── dvc.yaml               # DVC pipeline
│   └── requirements.txt
├── services/                   # Microservices
│   ├── recommendation-engine/  # ML inference
│   ├── user-api/              # User management
│   └── trip-planner/          # Trip orchestration
├── deployment-chart/           # Helm chart and Kubernetes manifests
│   ├── Chart.yaml             # Helm chart metadata
│   ├── values.yaml            # Helm configuration
│   ├── templates/              # Kubernetes manifests
│   └── argocd/                # ArgoCD Application
├── docker-compose.yml         # Local development
├── dvc.yaml                   # DVC configuration
├── README.md                  # This file
├── SETUP.md                   # Detailed setup guide
└── setup.sh                   # Automated setup script
```

## 🔐 Security Best Practices

- ✅ Environment variables for secrets
- ✅ Kubernetes secret management ready
- ✅ Service-to-service authentication (ready for mTLS)
- ✅ Health checks prevent traffic to unhealthy pods
- ✅ Resource limits prevent DoS attacks
- ✅ RBAC ready for Kubernetes

## 🔄 Continuous Improvements

Planned enhancements:
- [ ] Add Prometheus metrics exporters
- [ ] Integrate Grafana dashboards
- [ ] Add network policies
- [ ] Implement service mesh (Istio)
- [ ] Add canary deployments
- [ ] Implement blue-green deployments
- [ ] Add distributed tracing (Jaeger)
- [ ] ML model A/B testing

## 📚 Learning Resources

This project teaches:
1. **Kubernetes**: Deployments, Services, ConfigMaps, Secrets
2. **Helm**: Chart creation, templating, values management
3. **ArgoCD**: GitOps principles, continuous deployment
4. **GitHub Actions**: Workflow automation, CI/CD
5. **MLOps**: Model training, versioning, serving
6. **Docker**: Multi-stage builds, image optimization
7. **Microservices**: Service communication, scalability

## 🤝 Contributing

To enhance this portfolio:
1. Add monitoring (Prometheus + Grafana)
2. Implement service mesh
3. Add integration tests
4. Create deployment strategies (canary, blue-green)
5. Add security scanning
6. Implement cost optimization

## 📞 Support

See SETUP.md for detailed configuration and troubleshooting.

---

**This project demonstrates production-ready DevOps practices suitable for any scale organization.**
