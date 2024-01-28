.PHONY: *

# Project dirs:
ifeq ($(OS),Windows_NT)
PROJECT_DIR ?= $(shell cd)
BE_DIR ?= $(shell cd $(PROJECT_DIR) && cd backend && cd)
APP_DIR ?= $(shell cd $(BE_DIR) && cd app && cd)
MIG_DIR ?= $(shell cd $(APP_DIR) && cd db\migrations && cd)
TEST_DIR ?= $(shell cd $(BE_DIR) && cd tests && cd)
DOTENV ?= $(BE_DIR)\.env
else
PROJECT_DIR   ?= $(shell pwd)
BE_DIR ?= $(shell cd $(PROJECT_DIR) && cd backend && pwd)
APP_DIR ?= $(shell cd $(BE_DIR) && cd app && pwd)
MIG_DIR ?= $(shell cd $(APP_DIR) && cd db/migrations && pwd)
TEST_DIR ?= $(shell cd $(BE_DIR) && cd tests && pwd)
DOTENV ?= $(BE_DIR)/.env
endif


# Load dotenv:
ifeq ($(OS),Windows_NT)
ENV_CMD := powershell -command "& {foreach ($env_var in Get-Content $DOTENV) { $env_var -as [System.Collections.DictionaryEntry]; }}"
else
ENV_CMD := export
endif
include $(DOTENV)
export $(shell $(ENV_CMD))


# Fast onboarding setup:
onboarding: # Clone the repo, copy the template dotenv to a new .env file and run this command
	docker compose -f docker-compose.yml down
	docker compose -f docker-compose.yml up db -d
	cd $(BE_DIR) && pip install -r requirements-dev.txt

resume:
	docker compose -f docker-compose.yml up db -d

## Compose context commands (run infra on compose as context to run app on IDE or container
loc-start:  ## Run compose with all infra context except the API we want to run in IDE
	docker compose -f docker-compose.yml up db -d

loc-start-clean: ## Drop the DB then run infra context except API (to be ran from IDE)
	docker compose -f docker-compose.yml down --remove-orphans
	docker compose -f docker-compose.yml up db -d
	make mig-up

cont-start: ## Run inside docker container
	docker compose -f docker-compose.yml down --remove-orphans
	docker compose -f docker-compose.yml up db -d
	make mig-up
	docker compose -f docker-compose.yml up server

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
	docker volume rm pg-db-minimal

d-bash: ## Enter bash console in dockerized backend container
	docker compose run backend sh

d-pg: ## Enter Postgres console inside dockerized backend container
	docker exec db psql -h localhost -U postgres --dbname=postgres

d-reset-db: ## Resets the database and run migrations. After running this command, as the volume is not persistent you should get an empty db
	docker compose down
	make loc-start
	sleep 3
	make mig-up


## Requirements install
reqs-prod: ## Install prod only libraries (prod only; everywhere else you need dev libraries)
	cd $(BE_DIR) && pip install -r requirements.txt

reqs-dev: ## Install prod and non-prod libraries
	cd $(BE_DIR) && pip install -r requirements-dev.txt


## FastAPI commands
fapi-run: ## Run FastAPI server locally, no debug and in port default
	cd $(APP_DIR) && python -m uvicorn main:app --reload

fapi-debug: ## Run FastAPI server locally, debugging.
	cd $(APP_DIR) && python -m uvicorn main:app --debug


# Alembic migrations
mig-up: ## Run migrations
	alembic -c backend/alembic.ini upgrade head

mig-down: ## Run migrations
	alembic -c backend/alembic.ini downgrade base

ifeq ($(OS),Windows_NT)
    MIGRATION_NAME ?= $(shell powershell -c "$$mig_name = Read-Host 'Migration name? Example: removing column id.'; Write-Output $$mig_name")
else
    MIGRATION_NAME ?= $(shell bash -c 'read -p "Migration name? Example: removing column id." mig_name; echo $$mig_name')
endif
mig-gen: ## Auto generate migrations. Add existence validations after, before upgrading!
	alembic -c backend/alembic.ini revision --autogenerate -m "$(MIGRATION_NAME)"


### Yet to apply commands
#
#test:
#	cd $(TEST_DIR) && pytest -v --cov=.
#
#test-unit:
#	cd $(TEST_DIR) && pytest -v tests/unit --cov=.
#
#test-int:
#	cd $(TEST_DIR) && pytest -v tests/integration
#
#test-missing:
#	cd $(TEST_DIR) && pytest --cov=. --cov-report term-missing
#
#test-cov80:
#	cd $(TEST_DIR) && pytest --cov=. --cov-fail-under=80
#
#cli:
#	python app/cli.py
#
#precommit:
#	pre-commit run --all-files --show-diff-on-failure
