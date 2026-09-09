# Development & Deployment Checklist

## Pre-Deployment Checklist

### Code Quality
- [ ] All services pass linting (flake8/pylint)
- [ ] Unit tests pass with >80% coverage
- [ ] Integration tests pass
- [ ] Security scanning passes
- [ ] No hardcoded secrets or credentials
- [ ] Dependency vulnerabilities checked

### Docker & Containers
- [ ] All Dockerfiles use specific base image versions
- [ ] Multi-stage builds implemented
- [ ] Image size optimized
- [ ] Images tested locally
- [ ] Images scanned for vulnerabilities
- [ ] Push to Docker registry successful

### Kubernetes & Helm
- [ ] Helm chart syntax valid (`helm lint k8s/`)
- [ ] All templates render correctly (`helm template`)
- [ ] Resource limits/requests set appropriately
- [ ] Health checks configured
- [ ] Ingress configured (if needed)
- [ ] Persistent volume claims configured
- [ ] RBAC permissions defined

### MLOps
- [ ] Model training script tested locally
- [ ] Model evaluation metrics recorded
- [ ] DVC pipeline reproduces consistently
- [ ] Model versioning working
- [ ] Model can be loaded in production

### Configuration
- [ ] Environment variables documented
- [ ] Secrets stored in Kubernetes secrets
- [ ] ConfigMaps for non-sensitive config
- [ ] Database migrations planned
- [ ] Backup strategy defined

### GitOps
- [ ] All infrastructure in Git
- [ ] ArgoCD Application manifest validated
- [ ] Git repo is single source of truth
- [ ] Branch protection rules configured
- [ ] Code review process defined

## Deployment Steps

### First-Time Setup
```bash
# 1. Create namespace
kubectl create namespace travel-app

# 2. Install ArgoCD (if not already done)
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# 3. Create ArgoCD Application
kubectl apply -f k8s/argocd/application.yaml

# 4. Wait for sync
argocd app wait travel-app
```

### Regular Deployments
```bash
# 1. Make changes to code or manifests
# 2. Commit and push to Git
# 3. GitHub Actions runs CI/CD
# 4. ArgoCD automatically syncs
# 5. Verify deployment
kubectl get all -n travel-app
```

### Rolling Back
```bash
# If deployment fails, revert Git commit
git revert <commit-hash>
git push origin main

# Or use ArgoCD
argocd app sync travel-app --revision <git-commit>
```

## Post-Deployment Verification

### Service Health
```bash
# Check pod status
kubectl get pods -n travel-app

# Check service endpoints
kubectl get svc -n travel-app

# View logs
kubectl logs -n travel-app -l app=trip-planner -f
```

### Application Health
```bash
# Test recommendation endpoint
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

# Test user creation
curl -X POST http://localhost:8002/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "age": 30,
    "budget": 3000,
    "preferred_activities": ["Beach"]
  }'
```

### Monitoring
- [ ] Check CPU/Memory usage is reasonable
- [ ] No error spikes in logs
- [ ] Request latency acceptable
- [ ] Database connections healthy
- [ ] External service integrations working

## Troubleshooting Guide

### Pod not starting
```bash
# Check pod events
kubectl describe pod <pod-name> -n travel-app

# Check logs
kubectl logs <pod-name> -n travel-app

# Check resource limits
kubectl top pods -n travel-app
```

### Service not responding
```bash
# Test service connectivity
kubectl exec -it <pod-name> -n travel-app -- \
  curl http://recommendation-engine:8000/health

# Check DNS
kubectl exec -it <pod-name> -n travel-app -- \
  nslookup recommendation-engine
```

### Database connection errors
```bash
# Check database pod
kubectl get pod -n travel-app -l app=postgres

# Test connection
kubectl run psql-test --image=postgres:15-alpine --rm -it -- \
  psql -h postgres -U travel_user -d travel_db -c "SELECT 1"
```

### ArgoCD sync issues
```bash
# Check sync status
argocd app get travel-app

# View sync logs
argocd app logs travel-app

# Manual sync
argocd app sync travel-app --force
```

## Performance Tuning

### Scaling
```bash
# Increase replicas
kubectl scale deployment trip-planner -n travel-app --replicas=5

# Set up autoscaling (if configured in Helm)
kubectl get hpa -n travel-app
```

### Resource optimization
- Adjust resource requests/limits in values.yaml
- Monitor actual usage with `kubectl top`
- Scale down if over-provisioned
- Scale up if approaching limits

## Security Hardening

### Before production
- [ ] Enable RBAC
- [ ] Configure network policies
- [ ] Set up ingress with TLS
- [ ] Implement pod security policies
- [ ] Rotate all secrets and credentials
- [ ] Enable audit logging
- [ ] Set up backup strategy

## Monitoring & Alerts

### Key metrics to monitor
- Pod CPU and memory usage
- Request latency
- Error rates
- Database connection pool
- Model inference time

### Set up alerts for
- Pod crashes
- High error rate
- Slow response times
- Resource limit exhaustion
- Deployment failures

## Maintenance

### Regular tasks
- [ ] Review logs weekly
- [ ] Update dependencies monthly
- [ ] Retrain models weekly/monthly
- [ ] Backup database daily
- [ ] Review security alerts
- [ ] Test disaster recovery

### Monthly reviews
- [ ] Analyze performance metrics
- [ ] Review cost optimization
- [ ] Update documentation
- [ ] Plan capacity expansion
- [ ] Review and rotate secrets
