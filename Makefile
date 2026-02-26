.PHONY: help build up down logs clean init-aws test

help:
	@echo "Creator Dashboard - Available commands:"
	@echo "  make build      - Build Docker images"
	@echo "  make up         - Start all services"
	@echo "  make down       - Stop all services"
	@echo "  make logs       - View logs"
	@echo "  make clean      - Clean up containers and volumes"
	@echo "  make init-aws   - Initialize AWS resources"
	@echo "  make test       - Run tests"

build:
	docker-compose build

up:
	docker-compose up -d
	@echo "Services started!"
	@echo "Frontend: http://localhost:3000"
	@echo "Backend API: http://localhost:8000"
	@echo "API Docs: http://localhost:8000/docs"

down:
	docker-compose down

logs:
	docker-compose logs -f

clean:
	docker-compose down -v
	docker system prune -f

init-aws:
	chmod +x scripts/init-aws.sh
	./scripts/init-aws.sh

test:
	docker-compose exec backend pytest
	docker-compose exec frontend npm test
