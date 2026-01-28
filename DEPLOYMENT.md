# Deployment Guide

This guide covers various deployment options for AgriTrade Pro, from local development to production cloud deployments.

## Table of Contents

- [Local Development](#local-development)
- [Docker Deployment](#docker-deployment)
- [Cloud Deployments](#cloud-deployments)
- [Environment Configuration](#environment-configuration)
- [Security Considerations](#security-considerations)
- [Monitoring and Logging](#monitoring-and-logging)
- [Troubleshooting](#troubleshooting)

## Local Development

### Prerequisites
- Python 3.8 or higher
- Git
- Google Gemini API key

### Quick Setup
```bash
# Clone repository
git clone https://github.com/your-username/agritrade-pro.git
cd agritrade-pro

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.template .env
# Edit .env with your API keys

# Run application
streamlit run app.py
```

### Development Server
```bash
# Run with custom port
streamlit run app.py --server.port 8502

# Run with debug mode
streamlit run app.py --logger.level debug

# Run with auto-reload
streamlit run app.py --server.runOnSave true
```

## Docker Deployment

### Single Container
```bash
# Build image
docker build -t agritrade-pro .

# Run container
docker run -p 8501:8501 --env-file .env agritrade-pro
```

### Docker Compose (Recommended)
```bash
# Development
docker-compose up -d

# Production with nginx
docker-compose --profile production up -d

# View logs
docker-compose logs -f agritrade-pro

# Stop services
docker-compose down
```

### Docker Environment Variables
```bash
# Create .env file for Docker
cat > .env << EOF
GEMINI_API_KEY=your_api_key_here
ENVIRONMENT=production
DEBUG=false
USE_DYNAMODB=false
EOF
```

## Cloud Deployments

### Streamlit Cloud

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Deploy to Streamlit Cloud"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Configure secrets in the dashboard
   - Deploy automatically

3. **Configure Secrets**
   ```toml
   # .streamlit/secrets.toml
   GEMINI_API_KEY = "your_api_key_here"
   ENVIRONMENT = "production"
   DEBUG = false
   ```

### Heroku

1. **Prepare Heroku Files**
   ```bash
   # Create Procfile
   echo "web: streamlit run app.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile
   
   # Create runtime.txt
   echo "python-3.11.0" > runtime.txt
   ```

2. **Deploy to Heroku**
   ```bash
   # Install Heroku CLI and login
   heroku login
   
   # Create app
   heroku create your-app-name
   
   # Set environment variables
   heroku config:set GEMINI_API_KEY=your_api_key_here
   heroku config:set ENVIRONMENT=production
   
   # Deploy
   git push heroku main
   ```

### AWS Deployment

#### AWS ECS (Elastic Container Service)

1. **Build and Push to ECR**
   ```bash
   # Create ECR repository
   aws ecr create-repository --repository-name agritrade-pro
   
   # Get login token
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com
   
   # Build and tag image
   docker build -t agritrade-pro .
   docker tag agritrade-pro:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/agritrade-pro:latest
   
   # Push image
   docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/agritrade-pro:latest
   ```

2. **Create ECS Task Definition**
   ```json
   {
     "family": "agritrade-pro",
     "networkMode": "awsvpc",
     "requiresCompatibilities": ["FARGATE"],
     "cpu": "256",
     "memory": "512",
     "executionRoleArn": "arn:aws:iam::123456789012:role/ecsTaskExecutionRole",
     "containerDefinitions": [
       {
         "name": "agritrade-pro",
         "image": "123456789012.dkr.ecr.us-east-1.amazonaws.com/agritrade-pro:latest",
         "portMappings": [
           {
             "containerPort": 8501,
             "protocol": "tcp"
           }
         ],
         "environment": [
           {
             "name": "ENVIRONMENT",
             "value": "production"
           }
         ],
         "secrets": [
           {
             "name": "GEMINI_API_KEY",
             "valueFrom": "arn:aws:secretsmanager:us-east-1:123456789012:secret:agritrade-pro/api-keys"
           }
         ]
       }
     ]
   }
   ```

#### AWS Lambda (Serverless)

1. **Install Serverless Framework**
   ```bash
   npm install -g serverless
   npm install serverless-python-requirements
   ```

2. **Create serverless.yml**
   ```yaml
   service: agritrade-pro
   
   provider:
     name: aws
     runtime: python3.9
     region: us-east-1
     environment:
       ENVIRONMENT: production
   
   functions:
     app:
       handler: lambda_handler.handler
       events:
         - http:
             path: /{proxy+}
             method: ANY
   
   plugins:
     - serverless-python-requirements
   ```

### Google Cloud Platform

#### Cloud Run

1. **Build and Deploy**
   ```bash
   # Enable APIs
   gcloud services enable run.googleapis.com
   gcloud services enable cloudbuild.googleapis.com
   
   # Deploy
   gcloud run deploy agritrade-pro \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars ENVIRONMENT=production
   ```

2. **Set Secrets**
   ```bash
   # Create secret
   echo "your_api_key_here" | gcloud secrets create gemini-api-key --data-file=-
   
   # Update service with secret
   gcloud run services update agritrade-pro \
     --update-secrets GEMINI_API_KEY=gemini-api-key:latest
   ```

### Azure

#### Container Instances

```bash
# Create resource group
az group create --name agritrade-pro-rg --location eastus

# Deploy container
az container create \
  --resource-group agritrade-pro-rg \
  --name agritrade-pro \
  --image your-registry/agritrade-pro:latest \
  --dns-name-label agritrade-pro \
  --ports 8501 \
  --environment-variables ENVIRONMENT=production \
  --secure-environment-variables GEMINI_API_KEY=your_api_key_here
```

## Environment Configuration

### Production Environment Variables
```bash
# Required
GEMINI_API_KEY=your_gemini_api_key
ENVIRONMENT=production

# Optional
DEBUG=false
USE_DYNAMODB=true
AWS_REGION=us-east-1
DYNAMODB_TABLE_NAME=agritrade-pro-trades

# Security
SECRET_KEY=your_secret_key_here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

### Database Configuration

#### SQLite (Development)
```bash
# Default configuration
SQLITE_PATH=data/mandi_setu.db
```

#### DynamoDB (Production)
```bash
# Enable DynamoDB
USE_DYNAMODB=true
AWS_REGION=us-east-1
DYNAMODB_TABLE_NAME=agritrade-pro-trades

# AWS Credentials (use IAM roles in production)
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
```

## Security Considerations

### API Keys and Secrets
- Never commit API keys to version control
- Use environment variables or secret management services
- Rotate API keys regularly
- Use least-privilege access policies

### Network Security
- Use HTTPS in production
- Configure proper CORS settings
- Implement rate limiting
- Use Web Application Firewall (WAF)

### Application Security
- Validate all user inputs
- Sanitize data before database operations
- Use secure session management
- Implement proper error handling

### Infrastructure Security
```bash
# Example security group (AWS)
aws ec2 create-security-group \
  --group-name agritrade-pro-sg \
  --description "Security group for AgriTrade Pro"

aws ec2 authorize-security-group-ingress \
  --group-name agritrade-pro-sg \
  --protocol tcp \
  --port 443 \
  --cidr 0.0.0.0/0

aws ec2 authorize-security-group-ingress \
  --group-name agritrade-pro-sg \
  --protocol tcp \
  --port 80 \
  --cidr 0.0.0.0/0
```

## Monitoring and Logging

### Application Monitoring
```python
# Add to app.py for production monitoring
import logging
import time
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)

# Performance monitoring
@st.cache_data
def monitor_performance():
    start_time = time.time()
    # Your function logic
    end_time = time.time()
    logging.info(f"Function executed in {end_time - start_time:.2f} seconds")
```

### Health Checks
```python
# health_check.py
import requests
import sys

def health_check():
    try:
        response = requests.get("http://localhost:8501/_stcore/health", timeout=10)
        if response.status_code == 200:
            print("✅ Application is healthy")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

if __name__ == "__main__":
    if not health_check():
        sys.exit(1)
```

### Log Aggregation
```yaml
# docker-compose.yml with logging
version: '3.8'
services:
  agritrade-pro:
    build: .
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
    volumes:
      - ./logs:/app/logs
```

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Find process using port
   lsof -i :8501
   
   # Kill process
   kill -9 <PID>
   
   # Or use different port
   streamlit run app.py --server.port 8502
   ```

2. **Memory Issues**
   ```bash
   # Monitor memory usage
   docker stats agritrade-pro
   
   # Increase container memory
   docker run -m 1g agritrade-pro
   ```

3. **Database Connection Issues**
   ```bash
   # Check database file permissions
   ls -la data/mandi_setu.db
   
   # Reset database
   rm data/mandi_setu.db
   # Restart application to recreate
   ```

4. **API Key Issues**
   ```bash
   # Verify environment variables
   env | grep GEMINI_API_KEY
   
   # Test API key
   curl -H "Authorization: Bearer $GEMINI_API_KEY" \
        https://generativelanguage.googleapis.com/v1/models
   ```

### Performance Optimization

1. **Caching**
   ```python
   # Use Streamlit caching
   @st.cache_data(ttl=3600)  # Cache for 1 hour
   def expensive_computation():
       # Your expensive operation
       pass
   ```

2. **Database Optimization**
   ```python
   # Use connection pooling
   # Optimize queries
   # Use indexes
   ```

3. **Resource Limits**
   ```yaml
   # docker-compose.yml
   services:
     agritrade-pro:
       deploy:
         resources:
           limits:
             cpus: '0.5'
             memory: 512M
           reservations:
             cpus: '0.25'
             memory: 256M
   ```

### Debugging

1. **Enable Debug Mode**
   ```bash
   export DEBUG=true
   streamlit run app.py --logger.level debug
   ```

2. **Check Logs**
   ```bash
   # Application logs
   tail -f logs/app.log
   
   # Docker logs
   docker logs -f agritrade-pro
   
   # System logs
   journalctl -u agritrade-pro -f
   ```

3. **Profile Performance**
   ```python
   # Add profiling
   import cProfile
   import pstats
   
   profiler = cProfile.Profile()
   profiler.enable()
   # Your code here
   profiler.disable()
   
   stats = pstats.Stats(profiler)
   stats.sort_stats('cumulative')
   stats.print_stats()
   ```

## Backup and Recovery

### Database Backup
```bash
# SQLite backup
cp data/mandi_setu.db data/backup_$(date +%Y%m%d_%H%M%S).db

# DynamoDB backup
aws dynamodb create-backup \
  --table-name agritrade-pro-trades \
  --backup-name agritrade-pro-backup-$(date +%Y%m%d)
```

### Application Backup
```bash
# Create backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="backups/$DATE"

mkdir -p $BACKUP_DIR
cp -r data/ $BACKUP_DIR/
cp -r logs/ $BACKUP_DIR/
cp .env $BACKUP_DIR/
tar -czf $BACKUP_DIR.tar.gz $BACKUP_DIR/
rm -rf $BACKUP_DIR/

echo "Backup created: $BACKUP_DIR.tar.gz"
```

For more deployment options and advanced configurations, refer to the specific cloud provider documentation and the project's GitHub repository.