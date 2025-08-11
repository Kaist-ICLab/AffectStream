# AffectStream Local Development Makefile

.PHONY: help start stop restart clean logs build topics

# Default target
help:
	@echo "AffectStream Local Development Commands:"
	@echo ""
	@echo "  start     - Start all services"
	@echo "  stop      - Stop all services"
	@echo "  restart   - Restart all services"
	@echo "  clean     - Stop and remove all data"
	@echo "  logs      - Show logs for all services"
	@echo "  build     - Rebuild all services"
	@echo "  topics    - Create default Kafka topics"
	@echo ""
	@echo "Service-specific logs:"
	@echo "  logs-producer    - Show producer logs"
	@echo "  logs-consumer    - Show consumer logs"
	@echo "  logs-kafka       - Show Kafka logs"

# Main commands
start:
	@echo "Starting AffectStream services..."
	docker-compose up -d

stop:
	@echo "Stopping AffectStream services..."
	docker-compose down

restart:
	@echo "Restarting AffectStream services..."
	docker-compose restart

clean:
	@echo "Cleaning up all data..."
	docker-compose down -v

logs:
	docker-compose logs -f

build:
	@echo "Building all services..."
	docker-compose build

# Service-specific logs
logs-producer:
	docker-compose logs -f producer

logs-consumer:
	docker-compose logs -f consumer

logs-kafka:
	docker-compose logs -f kafka

# Kafka topic management
topics:
	@echo "Creating default Kafka topics..."
	docker-compose exec kafka kafka-topics --bootstrap-server localhost:9092 --create --topic chest --partitions 6 --replication-factor 1 --if-not-exists
	docker-compose exec kafka kafka-topics --bootstrap-server localhost:9092 --list
