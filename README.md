# AIOps Module 3 Assignment: Infrastructure & Containerization

This repository contains the code, configuration manifests, evidence screenshots, and final report for the AIOps Module 3 assignment covering Docker, Docker Compose, and Kubernetes.

---

## Repository Structure & File Functionality

### Root Directory
* **`AIOps_2.pdf`**: Comprehensive two-page report detailing methodologies, analysis, and empirical evidence for all assignment questions.

### `Q1/` (Docker & Multi-Stage Builds)
* **`Dockerfile`**: Naive single-stage Docker build configuration for packaging the spam-detection REST API.
* **`Dockerfile.multi`**: Optimized multi-stage Docker build file designed to minimize production image size.
* **`api.py`**: FastAPI application serving text classification predictions using a trained TF-IDF and Naive Bayes pipeline.
* **`requirements.txt`**: List of Python package dependencies required for the API execution environment.
* **`model.joblib`**: Serialized machine learning pipeline trained on the synthetic spam dataset.
* **`spam_dataset.csv`**: Deterministic synthetic dataset generated for training and testing the classification model.

### `Q2/` (Docker Compose & Caching)
* **`docker-compose.yml`**: Orchestration manifest defining multi-container networking between the API service and the Redis cache.
* **`api.py`**: Modified FastAPI application integrated with Redis to check cache hits and reduce inference latency.
* **`Dockerfile.multi`**: Multi-stage build file used to containerize the API service for Docker Compose execution.

### `Q3/` (Kubernetes Indexed Jobs)
* **`job.yaml`**: Kubernetes Indexed Job manifest configured with custom parallelism and Downward API fields for shard data validation.
* **`validator.py`**: Python script executed inside job pods to parse partitioned CSV shards and quantify malformed records.

### `Q4/` (Kubernetes Deployments, Self-Healing & Rolling Updates)
* **`deployment.yaml`**: Kubernetes Deployment and Service manifests specifying pod replicas, CPU resource constraints, and readiness probes.
* **`api.py`**: Updated FastAPI application featuring version indicators to test zero-downtime rolling updates.
* **`Dockerfile.multi`**: Multi-stage build file used to compile versioned image tags (`v1` and `v2`) for the deployment lifecycle.

* There is a folder named "evidence" in each of the above folders which consists of the screenshots from the terminal which were used to set up and run the code.
---

## Setup and Execution Instructions

Assuming you are currently at the root of the `Assignment-02` directory, run the terminal commands below to set up, deploy, and evaluate each component:

### 1. Question 1 & Question 4: Build and Load Docker Images
Build the container images locally and load them into Minikube for cluster deployment:
```bash
cd Q4
docker build -t spam-api:v1 -f Dockerfile.multi .
minikube image load spam-api:v1
```

### 2. Question 2: Multi-Container Orchestration with Docker Compose
Bring up the multi-container API and Redis caching stack:
```bash
cd ../Q2
docker compose up --build
```

### 3. Question 3: Kubernetes Indexed Job (Shard Validation)
Deploy the indexed batch job, verify parallelism via concurrent pod execution ages, and extract shard logs:
```bash
cd ../Q3
kubectl apply -f job.yaml
kubectl get pods -o wide
for i in {0..7}; do
  kubectl logs -l "job-name=validate-shards,batch.kubernetes.io/job-completion-index=$i"
done
```

### 4. Question 4: Kubernetes Deployments (Self-Healing & Rolling Updates)
Test self-healing through manual pod deletion and perform a zero-downtime rolling update to `v2`:
```bash
cd ../Q4
kubectl apply -f deployment.yaml
kubectl get pods
kubectl delete pod <PASTE_POD_NAME_HERE>
kubectl get pods

# Build and load the v2 image for the rolling update
docker build -t spam-api:v2 -f Dockerfile.multi .
minikube image load spam-api:v2

# Trigger rollout and verify status/history
kubectl set image deployment/spam-api-deployment api=spam-api:v2
kubectl rollout status deployment/spam-api-deployment
kubectl rollout history deployment/spam-api-deployment
```
