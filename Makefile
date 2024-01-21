.PHONY: *

# Env vars
APP			?= backend
SRC_DIR		?= api
BUILD_TAG	?= local

# Win compatibility:
ifeq ($(OS),Windows_NT)
	WORKDIR   ?= $(shell cd)
    ENV_FILE := $(APP)\.env
else
    WORKDIR   ?= $(shell pwd)
    ENV_FILE := $(APP)/.env
endif

include $(ENV_FILE)

VARS:=$(shell sed -ne 's/ *\#.*$$//; /./ s/=.*$$// p' $(ENV_FILE) )
#$(foreach v,$(VARS),$(eval $(shell echo export $(v)="$($(v))")))

vars:
	echo $(VARS)



## Makefile help and checks
#help: ## Show this help.
#	@grep -h -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
#
#check-deps: ## Check if Docker is installed.
#ifeq ($(strip $(DOCKER)),)
#	@echo "Docker is not available. Please install Docker."
#	@exit 1
#endif
#
#ifeq ($(shell docker compose 2> /dev/null),)
#	@echo "Docker version `Docker --version` is too old. Please upgrade to use Docker compose v2."
#	@exit 1
#endif
#
## Docker and Compose commands
#build-docker: check-deps ## Build inside docker container
#	$(DOCKER) build --build-arg GIT_CREDS=$$GIT_CREDS --tag $(APP):$(BUILD_TAG) -f Dockerfile .
#
#start-local: check-deps  ## Run compose with all infra context except the API we want to run in IDE
#	$(DOCKER) compose -f docker-compose.yml up db -d
#
#start-clean-local: check-deps  ## Drop the DB then run infra context except API (to be ran from IDE)
#	$(DOCKER) compose -f docker-compose.yml down --remove-orphans
#	$(DOCKER) compose -f docker-compose.yml up db -d
#
#start: check-deps ## Run inside docker container
#	$(DOCKER) compose -f docker-compose.yml down --remove-orphans
#	$(DOCKER) compose -f docker-compose.yml up db -d
#	# ----When finished, migra command goes here----
#	# ----When finished migrations, uvicorn command goes here----
#	$(DOCKER) compose -f docker-compose.yml up app
#
#stop: check-deps ## Stop docker container
#	$(COMPOSE) -f docker-compose.yml down --remove-orphans
#
## More Docker commands (check and delete repetitions)
#d-build: ## Build dockerized env and run app in the background
#	$(COMPOSE) build
#
#d-build-nc:  ## Build docker no cache
#	$(COMPOSE) build --no-cache
#
#d-up: ## Run dockerized in the background
#	$(COMPOSE) up --remove-orphans
#
#d-stop: ## Stop backend container
#	$(COMPOSE) stop
#
#d-rm-container:  ## Remove backend container
#	$(COMPOSE) rm backend
#
#d-rm-db:  ## Remove backend db
#	$(COMPOSE) -f docker-compose.yml down --remove-orphans
#	$(DOCKER) volume rm db
#
#d-bash: ## Enter bash console in dockerized backend container
#	$(COMPOSE) run backend sh
#
#d-pg: ## Enter Postgres console inside dockerized backend container
#	$(COMPOSE) exec db psql -h localhost -U postgres --dbname=creatorspace
#
#reset-db: ## Resets the database and run migrations. After running this command, as the volume is not persistent you should get an empty db
#	$(COMPOSE) down
#	make start-local
#	sleep 3
#	make migrate-up
#
## Requirements install
#reqs-prod: ## Install prod only libraries (prod cicd only; everywhere else you need dev libraries)
#	pip install -r requirements.txt
#
#reqs-dev: ## Install prod and non-prod libraries
#	pip install -r requirements-dev.txt
#
#
## Alembic migrations
#mig-up: ## Run migrations
#	cd $(WORKDIR)/$(SRC_DIR) && $(FLASK) db upgrade
#
#mig-down: ## Run migrations
#	cd $(WORKDIR)/$(SRC_DIR) && $(FLASK) db downgrade
#
#MIGRATION_NAME ?= $(shell bash -c 'read -p "Migration name? Example: removing column id." mig_name; echo $$mig_name')
#mig-gen: ## Auto generate migrations. Add existence validations after, before upgrading!
#	@clear
#	cd $(WORKDIR)/$(SRC_DIR) && alembic revision --autogenerate -m "$(MIGRATION_NAME)"
#
## FastAPI commands
#fapi-run: ## Run FastAPI server locally, no debug and in port default
#	cd $(WORKDIR)/$(SRC_DIR) && python -m uvicorn main:app
#
#fapi-debug: ## Run FastAPI server locally, debugging. Ensure you set the port in your env file.
#	$(FLASK) --app $(WORKDIR)/$(SRC_DIR)/app run --host ${FLASK_HOST} --port=$(PORT) --debug
