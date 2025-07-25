Here’s a **cleaned-up and properly formatted** version of your `README.md` to make it readable, professional, and informative:

---

# 🩻 End-to-End Chest Cancer Classification using MLflow & DVC

This project demonstrates an end-to-end workflow for image classification (Chest Cancer Detection) using CNNs, orchestrated with **DVC** for pipeline management and **MLflow** for experiment tracking. It includes configuration management, data versioning, experiment tracking, and deployment via Docker & AWS.

---

## 📌 Project Structure Overview

### ✅ Workflow Steps:

1. **Update `config.yaml`**
2. **Update `secrets.yaml`** *(Optional)*
3. **Update `params.yaml`**
4. **Define Configuration Entities** (`config_entity.py`)
5. **Update Configuration Manager** (`configuration.py`)
6. **Implement Components** (data ingestion, model training, etc.)
7. **Create Pipelines** (`pipeline/`)
8. **Run the Project with `main.py`**
9. **Define Pipelines in `dvc.yaml`**
10. **Track Experiments using MLflow**
11. **Document Everything**

---

## 🔁 Workflow Commands

### DVC Commands:

```bash
dvc init           # Initialize DVC repo
dvc repro          # Run the entire pipeline
dvc dag            # Visualize pipeline as a DAG
```

### MLflow UI:

```bash
mlflow ui
```

---

## 📊 MLflow Tracking (via DagsHub)

To enable MLflow tracking on DagsHub, set these environment variables:

```bash
export MLFLOW_TRACKING_URI=https://dagshub.com/shubhanagrawal/End-to-End-Chest-Cancer-Classification-using-MLfLow-DVC.mlflow
export MLFLOW_TRACKING_USERNAME=shubhanagrawal
export MLFLOW_TRACKING_PASSWORD=<your-token>
```

> 🔐 Replace `<your-token>` with your actual MLflow token (keep it private in `.env` or GitHub secrets).

---

## 🔍 About MLflow & DVC

### MLflow:

* Production-grade experiment tracker.
* Logs metrics, parameters, models.
* Tags and versions your models.

### DVC:

* Lightweight experiment tracking and pipeline orchestration tool.
* Enables reproducible machine learning pipelines.
* Integrates with Git for data and model versioning.

---

## 🚀 AWS CI/CD Deployment with GitHub Actions

### Prerequisites:

* Create an **IAM user** with access to:

  * **EC2** (virtual machine)
  * **ECR** (Elastic Container Registry)

#### Required IAM Policies:

* `AmazonEC2FullAccess`
* `AmazonEC2ContainerRegistryFullAccess`

---

### Deployment Steps:

1. **Create ECR Repo**
   Save the URI:
   `566373416292.dkr.ecr.us-east-1.amazonaws.com/chicken`

2. **Create EC2 Ubuntu Machine**
   Install Docker on EC2:

   ```bash
   sudo apt-get update -y
   sudo apt-get upgrade
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   sudo usermod -aG docker ubuntu
   newgrp docker
   ```

3. **Configure EC2 as a Self-hosted GitHub Actions Runner**

   * Go to: `GitHub Repo → Settings → Actions → Runners → Add new self-hosted runner`
   * Select OS and follow the setup instructions.

4. **Set GitHub Secrets for CI/CD**

| Key                     | Value                                                 |
| ----------------------- | ----------------------------------------------        |
| `AWS_ACCESS_KEY_ID`     | *Your IAM access key*                                 |
| `AWS_SECRET_ACCESS_KEY` | *Your IAM secret key*                                 |
| `AWS_REGION`            | `us-east-1`                                           |
| `AWS_ECR_LOGIN_URI`     | `602206539389.dkr.ecr.ap-south-1.amazonaws.com/chest` |
| `ECR_REPOSITORY_NAME`   | `chicken` or your model repo name                      |

---

## 🛠 Technologies Used

* Python
* Convolutional Neural Networks (CNN)
* MLflow
* DVC
* GitHub Actions
* Docker
* AWS EC2 & ECR
* DagsHub

---

## 👨‍💻 Author

**Shubhan Agrawal**
📍 [GitHub](https://github.com/shubhanagrawal)
📧 Email: *add if desired*

---

Let me know if you'd like to add badges, images, or split the deployment section into a separate file.
