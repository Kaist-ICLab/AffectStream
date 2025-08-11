# AffectStream Local Development Setup

This Docker Compose setup provides a complete local testing environment for AffectStream without requiring AWS or Terraform dependencies. It includes all necessary components to run the entire system locally.

## 🏗️ Architecture Overview

The local setup includes:

- **Kafka**: Message broker for real-time data streaming
- **Zookeeper**: Coordination service for Kafka
- **PostgreSQL**: Database for storing consumer results
- **Producer**: HTTP server that publishes sensor data to Kafka
- **Consumer**: Processes Kafka messages and performs affect analysis
- **Simulator**: Locust-based load testing tool
- **Monitoring Stack**: Prometheus + Grafana for metrics and visualization
- **AKHQ**: Web UI for Kafka management
- **Schema Registry**: Avro schema management

## 🚀 Quick Start

### Prerequisites

- Docker (20.10+)
- Docker Compose (2.0+)
- At least 8GB RAM available for Docker
- Available ports: 3000, 5432, 8080, 8081, 8082, 8089, 8090, 9090, 9092

### Simple Setup

```bash
# Start all services
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Clean up everything (including data)
docker-compose down -v
```

## 🔗 Service Access Points

| Service | URL | Credentials | Description |
|---------|-----|-------------|-------------|
| **Producer API** | http://localhost:8080 | N/A | REST API for publishing sensor data |
| **Simulator UI** | http://localhost:8089 | N/A | Locust load testing interface |
| **AKHQ (Kafka UI)** | http://localhost:8090 | N/A | Kafka management and monitoring |
| **Grafana** | http://localhost:3000 | admin/admin | Monitoring dashboards |
| **Prometheus** | http://localhost:9090 | N/A | Metrics collection |
| **PostgreSQL** | localhost:5432 | postgres/postgres | Database access |
| **Kafka** | localhost:9092 | N/A | Kafka broker |

## 📊 Basic Usage

### 1. Create Kafka Topics

```bash
# Create topic for sensor data
docker-compose exec kafka kafka-topics --bootstrap-server localhost:9092 \
  --create --topic chest --partitions 6 --replication-factor 1
```

### 2. Test Components

```bash
# Test producer health
curl http://localhost:8080/actuator/health

# Check Kafka topics
docker-compose exec kafka kafka-topics --bootstrap-server localhost:9092 --list

# Access database
docker-compose exec postgres psql -U postgres -d affectstream
```

### 3. Monitor System

- **Locust UI**: http://localhost:8089 (Load testing)
- **Kafka UI**: http://localhost:8090 (Topic monitoring)  
- **Grafana**: http://localhost:3000 (Performance dashboards)

## 🔧 Configuration

Key environment variables can be modified in `docker-compose.yaml`:

```yaml
# Producer settings
KAFKA_HOST: kafka:29092
SPRING_PROFILES_ACTIVE: local

# Consumer settings  
TOPIC: chest
PARTITIONS: 6
WINDOW_SIZE: 2

# Database settings
POSTGRES_DB: affectstream
POSTGRES_USER: postgres
POSTGRES_PASSWORD: postgres
```

## 🧹 Cleanup

```bash
# Stop services
docker-compose down

# Stop and remove volumes (⚠️ deletes all data)
docker-compose down -v

# Remove images as well
docker-compose down -v --rmi all
```

## 🆚 Differences from Kubernetes/AWS Setup

| Feature | Kubernetes/AWS | Docker Compose Local |
|---------|----------------|---------------------|
| **Scalability** | High (auto-scaling) | Limited (manual scaling) |
| **Persistence** | Cloud storage | Local volumes |
| **Monitoring** | Cloud-native tools | Prometheus + Grafana |
| **Security** | IAM, RBAC | Basic container isolation |
| **Cost** | Pay-per-use | Free (local resources) |
| **Setup Time** | 30+ minutes | 5-10 minutes |
| **Dependencies** | AWS account, kubectl | Docker only |

---

This local setup provides a complete AffectStream environment without cloud dependencies, making development and testing more accessible and cost-effective.
