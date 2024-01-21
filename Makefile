.PHONY: *


# Env vars
APP			?=backend
SRC_DIR		?=app
BUILD_TAG	?=local


# Load dotenv:
ifeq ($(OS),Windows_NT)
	WORKDIR   ?= $(shell cd)
else
    WORKDIR   ?= $(shell pwd)
endif


## Compose context commands (run infra on compose as context to run app on IDE or container
loc-start:  ## Run compose with all infra context except the API we want to run in IDE
	docker compose -f docker-compose.yml up db -d

loc-start-clean: ## Drop the DB then run infra context except API (to be ran from IDE)
	docker compose -f docker-compose.yml down --remove-orphans
	docker compose -f docker-compose.yml up db -d

cont-start: ## Run inside docker container
	docker compose -f docker-compose.yml down --remove-orphans
	docker compose -f docker-compose.yml up db -d
	docker compose -f docker-compose.yml up server
# ----When finished, migra command goes here----
# ----When finished migrations, uvicorn command goes here----

cont-stop: check-deps ## Stop docker container
	docker compose -f docker-compose.yml down --remove-orphans


# Docker commands
d-build: ## Build dockerized env and run app in the background
	docker compose build

d-build-nc:  ## Build docker no cache
	docker compose build --no-cache

d-up: ## Run dockerized in the background
	docker compose up --remove-orphans

d-stop: ## Stop backend container
	docker compose stop

d-rm-container:  ## Remove backend container
	docker compose rm api

d-rm-db:  ## Remove backend db
	docker compose -f docker-compose.yml down --remove-orphans
	docker volume rm db

d-bash: ## Enter bash console in dockerized backend container
	docker compose run backend sh

d-pg: ## Enter Postgres console inside dockerized backend container
	docker exec db psql -h localhost -U postgres --dbname=postgres

d-reset-db: ## Resets the database and run migrations. After running this command, as the volume is not persistent you should get an empty db
	docker compose down
	make start-local
	sleep 3
	make migrate-up


## Requirements install
reqs-prod: ## Install prod only libraries (prod only; everywhere else you need dev libraries)
	pip install -r requirements.txt

reqs-dev: ## Install prod and non-prod libraries
	pip install -r requirements-dev.txt


## FastAPI commands
fapi-run: ## Run FastAPI server locally, no debug and in port default
	cd $(WORKDIR)/$(SRC_DIR) && python -m uvicorn main:app --reload

fapi-debug: ## Run FastAPI server locally, debugging. Ensure you set the port in your env file.
	cd $(WORKDIR)/$(SRC_DIR)/app run --host ${FLASK_HOST} --port=$(PORT) --debug


# Alembic migrations
mig-up: ## Run migrations
	cd $(WORKDIR)/$(SRC_DIR) && alembic db upgrade

mig-down: ## Run migrations
	cd $(WORKDIR)/$(SRC_DIR) && alembic db downgrade

MIGRATION_NAME ?= $(shell bash -c 'read -p "Migration name? Example: removing column id." mig_name; echo $$mig_name')
mig-gen: ## Auto generate migrations. Add existence validations after, before upgrading!
	@clear
	cd $(WORKDIR)/$(SRC_DIR) && alembic revision --autogenerate -m "$(MIGRATION_NAME)"


### Yet to apply commands
#
#test:
#	pytest -v --cov=.
#
#test-unit:
#	pytest -v tests/unit --cov=.
#
#test-int:
#	pytest -v tests/integration
#
#test-missing:
#	pytest --cov=. --cov-report term-missing
#
#test-cov80:
#	pytest --cov=. --cov-fail-under=80
#
#cli:
#	python app/cli.py
#
#precommit:
#	pre-commit run --all-files --show-diff-on-failure
