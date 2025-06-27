# 🧠 Brain Tasks App – Production Deployment on AWS

This project demonstrates production-ready deployment of a React application to AWS infrastructure using **Docker**, **ECR**, **EKS**, **CodePipeline**, **CodeBuild**, and **CloudWatch Logs**.

---

## 🚀 Application Overview


- Customized repo: [My Repo](https://github.com/ravneet12345/Brain-Tasks-App)
- Frontend: ReactJS (pre-built)
- Deployment Target: AWS EKS (Kubernetes)

---

## 📦 Dockerization

Since the React app is already built, we only need to serve the static files.

### Dockerfile:

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

### Build & Run Locally:

```bash
docker build -t brain-tasks-app .
docker run -p 80:3000 brain-tasks-app
```

---

## 🐳 AWS ECR (Elastic Container Registry)

### Create ECR Repository:

```bash
aws ecr create-repository   --repository-name brain-tasks-app   --region ap-south-1
```

### Build, Tag & Push Docker Image:

```bash
export ECR_URI=470397863283.dkr.ecr.ap-south-1.amazonaws.com/brain-tasks-app

docker build -t brain-tasks-app .
docker tag brain-tasks-app:latest $ECR_URI:latest

aws ecr get-login-password --region ap-south-1   | docker login --username AWS --password-stdin $ECR_URI

docker push $ECR_URI:latest
```

---

## ☸️ AWS EKS – Kubernetes Deployment

### deployment.yaml:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: brain-tasks-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: brain-tasks-app
  template:
    metadata:
      labels:
        app: brain-tasks-app
    spec:
      containers:
        - name: app
          image: 470397863283.dkr.ecr.ap-south-1.amazonaws.com/brain-tasks-app:latest
          ports:
            - containerPort: 3000
```

### service.yaml:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: brain-tasks-service
spec:
  selector:
    app: brain-tasks-app
  ports:
    - port: 80
      targetPort: 3000
  type: LoadBalancer
```

### Deploy to EKS:

```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

---

## 🛠️ AWS CodeBuild (CI/CD)

### ✅ File: [`buildspec.yml`](https://github.com/ravneet12345/Brain-Tasks-App/blob/prod/buildspec.yml)

```yaml
version: 0.2

phases:
  install:
    commands:
      - echo Installing kubectl...
      - curl -LO https://dl.k8s.io/release/v1.30.0/bin/linux/amd64/kubectl
      - chmod +x kubectl && mv kubectl /usr/local/bin/kubectl
      - echo Configuring kubectl for EKS...
      - aws eks update-kubeconfig --region us-east-1 --name Brain-task-cluster

  pre_build:
    commands:
      - echo Logging in to ECR...
      - aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 470397863283.dkr.ecr.us-east-1.amazonaws.com/brain-tasks-app

  build:
    commands:
      - echo Building Docker image...
      - docker build -t brain-tasks-app .
      - docker tag brain-tasks-app:latest 470397863283.dkr.ecr.us-east-1.amazonaws.com/brain-tasks-app:latest

  post_build:
    commands:
      - echo Pushing image to ECR...
      - docker push 470397863283.dkr.ecr.us-east-1.amazonaws.com/brain-tasks-app:latest
      - echo Deploying to EKS via kubectl...
      - kubectl apply -f deployment.yaml
      - kubectl apply -f service.yaml

artifacts:
  files:
    - deployment.yaml
    - service.yaml
```

---

## 🔄 CodePipeline

### Stages:

1. **Source** – GitHub (`prod` branch)
2. **Build & Deploy** – CodeBuild using `buildspec.yml`

> Deployment to EKS is handled by `kubectl set image` inside CodeBuild (no CodeDeploy used).

---

## 📊 CloudWatch Logs

- **CodeBuild logs** are automatically available in CloudWatch.
- Future enhancement: Add FluentD or CloudWatch Agent for EKS pod logs.

---

## 🌐 Access the App

After deploying, get the LoadBalancer URL:

```bash
kubectl get svc brain-tasks-service
```

Example output:

```bash
NAME                  TYPE           CLUSTER-IP      EXTERNAL-IP                                                               PORT(S)
brain-tasks-service   LoadBalancer   10.100.87.197   aaaaa1111bbb2222ccc3333ddd.elb.ap-south-1.amazonaws.com                80:30234/TCP
```

Visit the external IP or DNS to view the deployed React app.

---

## 📸 Screenshots

> *(Add these screenshots are added on doc):*
- CodePipeline success
- CodeBuild logs
- `kubectl get pods`
- `kubectl get svc`
- Browser screenshot of app running via LoadBalancer

---

## 📌 Notes

- ✅ React app is **pre-built**, no need to run `npm run build`.
- ✅ Docker only serves static `build/` files using `serve`.
- ✅ Pipeline is fully automated: GitHub → CodeBuild → ECR → EKS.
- ✅ LoadBalancer exposes app to internet on port 80 → 3000.

---
