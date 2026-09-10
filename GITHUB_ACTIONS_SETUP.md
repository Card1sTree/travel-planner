# GitHub Actions - Secret Configuration

To make the GitHub Actions workflows work, configure these secrets in your repository:

## 1. Docker Registry Secrets
**Repository Settings → Secrets and variables → Actions**

```
DOCKER_USERNAME: your-docker-hub-username
DOCKER_PASSWORD: your-docker-hub-token
```

### How to get Docker Hub token:
1. Go to https://hub.docker.com/settings/security
2. Create a new access token
3. Copy the token and paste in GitHub secrets

## 2. Kubernetes & ArgoCD Secrets

```
ARGOCD_SERVER: https://your-argocd-server.com
ARGOCD_TOKEN: <your-argocd-api-token>
```

### How to get ArgoCD token:
```bash
# Login to ArgoCD
argocd login <ARGOCD_SERVER>

# Generate API token
argocd account generate-token --account <your-account>
```

## 3. AWS Secrets (for DVC)

```
AWS_ACCESS_KEY_ID: <your-aws-access-key>
AWS_SECRET_ACCESS_KEY: <your-aws-secret-key>
```

### DVC Remote Configuration
```bash
# Configure S3 as DVC remote
dvc remote add -d myremote s3://your-bucket/dvc-storage
dvc remote modify myremote profile default
```

## 4. Slack Notifications (Optional)

```
SLACK_WEBHOOK: https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

### How to get Slack webhook:
1. Go to https://api.slack.com/apps
2. Create new app
3. Enable Incoming Webhooks
4. Create new webhook for your channel

## 5. Repository Variables (Optional)

Go to **Settings → Secrets and variables → Variables**

```
DOCKER_REGISTRY: docker.io
KUBERNETES_NAMESPACE: travel-app
PROJECT_NAME: travel-app
```

## GitHub Actions Files Overview

### .github/workflows/ci.yml
- **Trigger**: Push to main/develop
- **Functions**:
  - Runs tests on all services
  - Builds Docker images
  - Pushes images to Docker Hub
  - Triggers ArgoCD sync
- **Requires**: DOCKER_USERNAME, DOCKER_PASSWORD, ARGOCD_TOKEN

### .github/workflows/train-model.yml
- **Trigger**: Daily at 2 AM UTC or manual dispatch
- **Functions**:
  - Prepares training data
  - Trains ML model
  - Evaluates performance
  - Versions model with DVC
  - Pushes to Git
- **Requires**: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

### .github/workflows/deploy.yml
- **Trigger**: Changes to deployment-chart/ directory
- **Functions**:
  - Validates Kubernetes manifests
  - Syncs with ArgoCD
  - Checks deployment health
  - Sends Slack notifications
- **Requires**: ARGOCD_TOKEN, SLACK_WEBHOOK (optional)

### .github/workflows/setup.yml
- **Trigger**: Manual dispatch
- **Functions**:
  - Installs ArgoCD
  - Creates namespaces
  - Cleans up resources

## Testing Workflows Locally

### Using act (GitHub Actions locally)
```bash
# Install act
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Run workflow locally
act -j build -s DOCKER_USERNAME=youruser -s DOCKER_PASSWORD=yourtoken
```

## Debugging Failed Workflows

### View workflow logs
1. Go to **Actions** tab in GitHub
2. Click on the failed workflow
3. Click on the failed job
4. View detailed logs

### Common issues
- **Docker auth failed**: Check DOCKER_USERNAME and DOCKER_PASSWORD
- **ArgoCD sync failed**: Verify ARGOCD_TOKEN and server URL
- **Model training failed**: Check AWS credentials and DVC remote
- **Manifest validation failed**: Run `helm template` locally to check syntax

## Setting Up Notifications

### For failed deployments
Add your Slack channel to notifications:
1. Create Slack app webhook (see above)
2. Add SLACK_WEBHOOK to secrets
3. Uncomment Slack notification step in workflows

### Email notifications (GitHub native)
Go to **Settings → Notifications** to configure email alerts

## Security Best Practices

✅ **Never commit secrets** to Git  
✅ **Rotate tokens** regularly  
✅ **Use short-lived credentials** when possible  
✅ **Review workflow permissions** in Actions settings  
✅ **Restrict secrets** to required branches only  
✅ **Monitor secret usage** in Action logs  

## Next Steps

1. [ ] Create GitHub personal access token
2. [ ] Set up Docker Hub account
3. [ ] Configure AWS S3 bucket for DVC
4. [ ] Set up ArgoCD server
5. [ ] Add all secrets to GitHub repository
6. [ ] Run setup workflow
7. [ ] Monitor CI/CD in Actions tab
