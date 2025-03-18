# AffectStream: Kafka-based Real-time Affect Monitoring System using Wearable Sensors
Real-time affect monitoring is essential for personalized and adaptive applications in fields like education, healthcare, and customer service. However, existing systems often struggle with scalability and low-latency requirements for processing high-frequency sensor data. To address these challenges, we propose AffectStream, a Kafka-based real-time affect monitoring system that processes wearable sensor data through a cloud-based pub/sub architecture to the applications. AffectStream ensures scalability, fault tolerance, and personalized emotional state analysis. Its robust performance is demonstrated through trace-based evaluations using the WESAD dataset. This open-source framework advances real-time emotion recognition, paving the way for large-scale affective computing applications.

## Code Structure Overview
```
📦 AffectStream/
 ┣ 📂 analysis/
 ┣ 📂 components/
 ┣ 📂 infrastructure/
 ┣ 📜 .gitignore
 ┣ 📜 LICENSE
 ┗ 📜 README.md
 ```

### 1. `analysis/`
This folder contains sql script, performance evaluations, and experiment results.
- Contents
    - SQL script for querying data and extracting insights (`.sql`)
    - Jupyter notebook for result visualization (`.ipynb`)

### 2. `components/`
This folder contains the core application modules, including Kafka consumers, producers, and simulators.
- Contents
    - `consumer/`: Kafka consumers responsible for processing messages from topics.
    - `kafka_management/`: Handles Kafka configurations, including topic creation, monitoring, and security.
    - `producer/`: Kafka producers that publish messages to specified topics.
    - `simulator/`: Simulates real-time data streaming for testing and benchmarking.

### 3. `infrastructure/`
This folder manages the deployment of components from the `components/` folder and infrastructure configurations, including Kubernetes and Docker.
- Conents
    - `kubernetes/`: Contains Kubernetes manifests (`.yaml` files) for deploying and managing services, deployments, and networking.
    - `terraform/`: Infrastructure-as-Code (IaC) configurations for provisioning cloud resources such as databases, compute instances, and networking using Terraform.