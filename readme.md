# 👀 Brain Tasks App - Production Deployment on AWS

This project demonstrates a full CI/CD pipeline for deploying a React-based application using:

- **Docker**
- **Amazon ECR**
- **Amazon EKS (Kubernetes)**
- **AWS CodePipeline**
- **AWS CodeBuild**
- **AWS Lambda (for deployment to EKS)**
- **CloudWatch (for monitoring)**

---

## 🔧 Application Overview

- **Repository**: [Brain Tasks App GitHub](https://github.com/Vennilavan12/Brain-Tasks-App.git)
- **Port**: 3000 (React App)
- **Frontend**: React
- **Deployment Target**: Kubernetes via Amazon EKS

---

## 🚀 Deployment Architecture

```text
GitHub → CodePipeline → CodeBuild → Docker Image → ECR → Lambda → EKS
```

---

## 🗂️ Project Structure

```
.
├── Dockerfile
├── buildspec.yml
├── deployment.yaml
├── service.yaml
├── lambda/
│   └── handler.py
└── README.md
```

---

## 🐳 Dockerization

**Dockerfile**:

```Dockerfile
# Use an official Nginx image
FROM public.ecr.aws/nginx/nginx:alpine

# Remove default Nginx static assets
RUN rm -rf /usr/share/nginx/html/*

# Copy build output to Nginx's web directory
COPY dist/ /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx server
CMD ["nginx", "-g", "daemon off;"]
```

---

## ☘️ Kubernetes Configuration

**deployment.yaml**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: brain-tasks-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: brain-tasks
  template:
    metadata:
      labels:
        app: brain-tasks
    spec:
      containers:
      - name: brain-tasks-container
        image: <ECR_IMAGE_URI>
        ports:
        - containerPort: 80
```

**service.yaml**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: brain-tasks-service
spec:
  type: LoadBalancer
  selector:
    app: brain-tasks
  ports:
    - port: 80
      targetPort: 80
```

---

## 🏗️ CodeBuild Configuration

**buildspec.yml**

```yaml
version: 0.2

phases:
  install:
    commands:
      - curl -LO https://dl.k8s.io/release/v1.30.0/bin/linux/amd64/kubectl
      - chmod +x kubectl && mv kubectl /usr/local/bin/
      - aws eks update-kubeconfig --name Brain-task-cluster --region us-east-1

  pre_build:
    commands:
      - aws ecr get-login-password | docker login --username AWS --password-stdin <ECR_URI>

  build:
    commands:
      - docker build -t brain-tasks-app .
      - docker tag brain-tasks-app <ECR_IMAGE_URI>

  post_build:
    commands:
      - docker push <ECR_IMAGE_URI>
artifacts:
  files:
    - '**/*'
```

---

## 🧐 Lambda Deploy Script

**lambda/handler.py**

```python
import boto3
import subprocess
import os

def handler(event, context):
    job_id = event['CodePipeline.job']['id']
    try:
        subprocess.run([
            "aws", "eks", "update-kubeconfig",
            "--name", os.environ['CLUSTER_NAME'],
            "--region", os.environ['AWS_REGION']
        ], check=True)

        subprocess.run([
            "kubectl", "set", "image",
            f"deployment/{os.environ['DEPLOYMENT_NAME']}",
            f"{os.environ['CONTAINER_NAME']}={os.environ['ECR_IMAGE_URI']}"
        ], check=True)

        boto3.client('codepipeline').put_job_success_result(jobId=job_id)
    except Exception as e:
        boto3.client('codepipeline').put_job_failure_result(
            jobId=job_id,
            failureDetails={'message': str(e), 'type': 'JobFailed'}
        )
        raise
```

**Environment Variables:**

```
CLUSTER_NAME=Brain-task-cluster
DEPLOYMENT_NAME=brain-tasks-deployment
CONTAINER_NAME=brain-tasks-container
ECR_IMAGE_URI=470397863283.dkr.ecr.us-east-1.amazonaws.com/brain-tasks-app:latest
AWS_REGION=us-east-1
```

---

## 🔐 IAM Roles Required

- **CodeBuild Role**:

  - `ecr:*`
  - `eks:*`

- **Lambda Role**:

  - `eks:*`
  - `codepipeline:PutJob*`

- **CodePipeline Role**:

  - `codebuild:*`
  - `lambda:InvokeFunction`

---

## 📊 Monitoring with CloudWatch

- Enable CloudWatch logging in:
  - CodeBuild project settings
  - Lambda function config
  - EKS pod logs via FluentBit (optional)

---

## ✅ Outputs

- **GitHub Repository**: `https://github.com/<your-username>/brain-tasks-deploy`
- **Load Balancer ARN**: Copy from:
  ```bash
  kubectl get svc brain-tasks-service
  ```

---

## 📸 Screenshots to Include

- EKS Cluster running
- CodeBuild build logs
- Lambda function setup
- CodePipeline pipeline overview
- Web App accessible via Load Balancer

---

## 📞 Final Submission Checklist

-

---

> **Need Help?**\
> Let me know if you'd like a zipped bundle or infrastructure-as-code templates (Terraform/CDK).

download readme file

