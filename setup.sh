#!/bin/bash
# Setup script for Travel App DevOps project

set -e

echo "🚀 Travel App Setup Script"
echo "=========================="

# Check prerequisites
check_prerequisites() {
    echo "✓ Checking prerequisites..."
    
    command -v docker &> /dev/null || { echo "❌ Docker is required"; exit 1; }
    command -v docker-compose &> /dev/null || { echo "❌ Docker Compose is required"; exit 1; }
    command -v kubectl &> /dev/null || { echo "❌ kubectl is required"; exit 1; }
    command -v helm &> /dev/null || { echo "❌ Helm is required"; exit 1; }
    
    echo "✅ All prerequisites met"
}

# Setup local environment
setup_local() {
    echo ""
    echo "📦 Setting up local environment..."
    
    # Create models directory
    mkdir -p ml/models
    mkdir -p ml/data
    
    # Install Python dependencies
    python -m venv venv
    source venv/bin/activate || . venv/Scripts/activate
    pip install -r ml/requirements.txt
    
    # Train initial model
    echo "🤖 Training initial model..."
    python ml/train.py
    
    echo "✅ Local environment setup complete"
}

# Start Docker Compose
start_docker_compose() {
    echo ""
    echo "🐳 Starting Docker Compose..."
    
    docker-compose up -d
    
    echo "⏳ Waiting for services to be ready..."
    sleep 10
    
    echo "✅ Docker Compose started"
    echo "  - Recommendation Engine: http://localhost:8001/docs"
    echo "  - User API: http://localhost:8002/docs"
    echo "  - Trip Planner: http://localhost:8003/docs"
}

# Menu
show_menu() {
    echo ""
    echo "Setup Options:"
    echo "1. Check prerequisites only"
    echo "2. Setup local environment (Python + dependencies)"
    echo "3. Start Docker Compose services"
    echo "4. Full local setup (1+2+3)"
    echo "5. Setup Kubernetes cluster"
    echo "6. Deploy to Kubernetes"
    echo "0. Exit"
    echo ""
    read -p "Select option: " choice
    
    case $choice in
        1)
            check_prerequisites
            ;;
        2)
            setup_local
            ;;
        3)
            start_docker_compose
            ;;
        4)
            check_prerequisites
            setup_local
            start_docker_compose
            ;;
        5)
            echo "Installing kind and creating cluster..."
            # Install kind
            curl -Lo ./kind https://kind.sigs.k8s.io/dl/latest/kind-linux-amd64
            chmod +x ./kind
            sudo mv ./kind /usr/local/bin/
            
            # Create cluster
            kind create cluster --config kind-config.yaml
            echo "✅ Kubernetes cluster created"
            ;;
        6)
            echo "Installing ArgoCD..."
            kubectl create namespace argocd
            kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
            
            echo "Deploying Travel App..."
            kubectl create namespace travel-app
            kubectl apply -f k8s/argocd/application.yaml
            
            echo "✅ Deployment complete"
            echo "Access ArgoCD UI: kubectl port-forward svc/argocd-server -n argocd 8080:443"
            ;;
        0)
            echo "Exiting..."
            exit 0
            ;;
        *)
            echo "Invalid option"
            show_menu
            ;;
    esac
}

# Main
check_prerequisites
show_menu
