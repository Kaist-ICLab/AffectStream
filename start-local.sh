#!/bin/bash

# AffectStream Local Setup Startup Script
# This script starts the entire AffectStream environment locally

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=========================================="
echo "   AffectStream Local Setup"
echo -e "==========================================${NC}"

# Function to print status
print_status() {
    echo -e "${YELLOW}>>> $1${NC}"
}

# Function to print success
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

# Function to print error
print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed or not in PATH"
        exit 1
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed or not in PATH"
        exit 1
    fi
    
    # Check if Docker daemon is running
    if ! docker info &> /dev/null; then
        print_error "Docker daemon is not running. Please start Docker first."
        exit 1
    fi
    
    print_success "Prerequisites check passed"
}

# Check port availability
check_ports() {
    print_status "Checking port availability..."
    
    local ports=(3000 5432 8080 8081 8082 8089 8090 9090 9092 2181)
    local unavailable_ports=()
    
    for port in "${ports[@]}"; do
        if ss -tulwn | grep ":$port " > /dev/null 2>&1; then
            unavailable_ports+=($port)
        fi
    done
    
    if [ ${#unavailable_ports[@]} -ne 0 ]; then
        print_error "The following ports are already in use: ${unavailable_ports[*]}"
        echo "Please stop the services using these ports or modify docker-compose.yaml"
        exit 1
    fi
    
    print_success "All required ports are available"
}

# Build and start services
start_services() {
    print_status "Building and starting services..."
    
    # Pull latest images and build
    docker-compose pull
    docker-compose build
    
    # Start services
    docker-compose up -d
    
    print_success "Services started successfully"
}

# Wait for services to be ready
wait_for_services() {
    print_status "Waiting for services to be ready..."
    
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        echo -n "Attempt $attempt/$max_attempts: "
        
        # Check Kafka
        if docker-compose exec kafka kafka-broker-api-versions --bootstrap-server localhost:9092 > /dev/null 2>&1; then
            echo -e "${GREEN}Kafka is ready${NC}"
            break
        else
            echo "Kafka not ready yet..."
            sleep 10
            ((attempt++))
        fi
        
        if [ $attempt -gt $max_attempts ]; then
            print_error "Timeout waiting for services to be ready"
            echo "Check service logs with: docker-compose logs"
            exit 1
        fi
    done
    
    print_success "Core services are ready"
}

# Create default Kafka topics
create_topics() {
    print_status "Creating Kafka topics..."
    
    # Create chest topic for sensor data
    docker-compose exec kafka kafka-topics --bootstrap-server localhost:9092 \
        --create --topic chest --partitions 6 --replication-factor 1 \
        --if-not-exists
    
    # Create any additional topics as needed
    # docker-compose exec kafka kafka-topics --bootstrap-server localhost:9092 \
    #     --create --topic wrist --partitions 6 --replication-factor 1 \
    #     --if-not-exists
    
    print_success "Kafka topics created"
}

# Display service information
show_service_info() {
    echo ""
    echo -e "${BLUE}=========================================="
    echo "   AffectStream Services Ready!"
    echo -e "==========================================${NC}"
    echo ""
    echo -e "${YELLOW}Service URLs:${NC}"
    echo "  🌐 Producer API:     http://localhost:8080"
    echo "  📊 Simulator:       http://localhost:8089"
    echo "  🔍 Kafka UI (AKHQ): http://localhost:8090"
    echo "  📈 Grafana:         http://localhost:3000 (admin/admin)"
    echo "  📉 Prometheus:      http://localhost:9090"
    echo "  🗄️  PostgreSQL:      localhost:5432 (postgres/postgres)"
    echo ""
    echo -e "${YELLOW}Quick Commands:${NC}"
    echo "  📊 Check health:    ./health-check.sh"
    echo "  📋 View logs:       docker-compose logs -f"
    echo "  🛑 Stop services:   docker-compose down"
    echo "  🔄 Restart:         docker-compose restart <service>"
    echo ""
    echo -e "${YELLOW}Getting Started:${NC}"
    echo "  1. Open http://localhost:8089 to start load testing"
    echo "  2. Open http://localhost:3000 for monitoring dashboards"
    echo "  3. Open http://localhost:8090 to explore Kafka topics"
    echo ""
    echo -e "${GREEN}Setup completed successfully!${NC}"
}

# Cleanup function
cleanup() {
    if [ $? -ne 0 ]; then
        print_error "Setup failed. Cleaning up..."
        docker-compose down
    fi
}

# Set up trap for cleanup
trap cleanup EXIT

# Main execution
main() {
    echo "Starting AffectStream local setup..."
    echo ""
    
    check_prerequisites
    check_ports
    start_services
    wait_for_services
    create_topics
    show_service_info
    
    # Remove the cleanup trap since we succeeded
    trap - EXIT
}

# Parse command line arguments
case "${1:-start}" in
    "start")
        main
        ;;
    "stop")
        print_status "Stopping all services..."
        docker-compose down
        print_success "All services stopped"
        ;;
    "restart")
        print_status "Restarting all services..."
        docker-compose restart
        print_success "All services restarted"
        ;;
    "clean")
        print_status "Stopping and cleaning up all data..."
        docker-compose down -v
        print_success "Cleanup completed"
        ;;
    "logs")
        docker-compose logs -f "${2:-}"
        ;;
    "status")
        docker-compose ps
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|clean|logs|status}"
        echo ""
        echo "Commands:"
        echo "  start   - Start all services (default)"
        echo "  stop    - Stop all services"
        echo "  restart - Restart all services"
        echo "  clean   - Stop and remove all data"
        echo "  logs    - Show logs (optionally for specific service)"
        echo "  status  - Show service status"
        exit 1
        ;;
esac
