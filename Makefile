# Makefile for Greene County Property Finder
# Usage: make <target>

.PHONY: help install install-dev run test lint format clean docker-build docker-run fetch-data

# Default target
help:
	@echo "Greene County Property Finder - Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install        Install production dependencies"
	@echo "  make install-dev    Install development dependencies"
	@echo ""
	@echo "Development:"
	@echo "  make run            Run the Streamlit app"
	@echo "  make test           Run tests"
	@echo "  make test-cov       Run tests with coverage"
	@echo "  make lint           Run linting checks"
	@echo "  make format         Format code with Black"
	@echo ""
	@echo "Data:"
	@echo "  make fetch-data     Fetch Hunter/Lanesville parcel data"
	@echo "  make fetch-all      Fetch all Greene County data"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build   Build Docker image"
	@echo "  make docker-run     Run Docker container"
	@echo "  make docker-stop    Stop Docker container"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean          Remove cache and temp files"
	@echo "  make clean-data     Remove cached parcel data"

# =============================================================================
# Setup
# =============================================================================

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	pre-commit install

# =============================================================================
# Development
# =============================================================================

run:
	streamlit run app.py

test:
	pytest tests/ -v

test-cov:
	pytest tests/ -v --cov=. --cov-report=html --cov-report=term-missing
	@echo "Coverage report: htmlcov/index.html"

test-unit:
	pytest tests/ -v -m "not integration"

test-integration:
	pytest tests/ -v -m integration

lint:
	flake8 . --max-line-length=120 --exclude=venv,__pycache__,.git
	mypy . --ignore-missing-imports || true

format:
	black . --line-length=120
	isort . --profile=black --line-length=120

format-check:
	black . --check --line-length=120
	isort . --check --profile=black --line-length=120

# =============================================================================
# Data
# =============================================================================

fetch-data:
	python greene_county_fetcher.py --lanesville

fetch-all:
	python greene_county_fetcher.py

list-municipalities:
	python greene_county_fetcher.py --list

# =============================================================================
# Docker
# =============================================================================

docker-build:
	docker build -t greene-county-property-finder .

docker-run:
	docker run -d -p 8501:8501 -v $(PWD)/data:/app/data --name gcpf greene-county-property-finder

docker-stop:
	docker stop gcpf || true
	docker rm gcpf || true

docker-compose-up:
	docker-compose up -d

docker-compose-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

# =============================================================================
# Cleanup
# =============================================================================

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true

clean-data:
	rm -f data/*.json
	rm -rf data/.cache

clean-all: clean clean-data
	rm -rf venv
	rm -rf .venv
