# 👀 Brain Tasks App - Production Deployment on AWS

This project demonstrates a full CI/CD pipeline for deploying a React-based application using:

- **Docker**
- **Amazon ECR**
- **Amazon EKS (Kubernetes)**
- **AWS CodePipeline**
- **AWS CodeBuild**
- **CloudWatch (for monitoring)**

---

## 🔧 Application Overview

- **Repository**: [Brain Tasks App GitHub](https://github.com/Vennilavan12/Brain-Tasks-App.git)
- **Port**: 80 (React App)
- **Frontend**: React
- **Deployment Target**: Kubernetes via Amazon EKS

---

## 🚀 Deployment Architecture

```text
GitHub → CodePipeline → CodeBuild → Docker Image → ECR → EKS
```

---

## 🗂️ Project Structure

```
.
├── Dockerfile
├── buildspec.yml
├── deployment.yaml
├── service.yaml
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


---

## 🔐 IAM Roles Required

- **CodeBuild Role**:

  - `ecr:*`
  - `eks:*`

- **CodePipeline Role**:

  - `codebuild:*`
  - `lambda:InvokeFunction`

---

## 📊 Monitoring with CloudWatch

- Enable CloudWatch logging in:
- CodeBuild project settings
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
- CodePipeline pipeline overview
- Web App accessible via Load Balancer

---
