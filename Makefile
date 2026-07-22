help:
	@echo
	@echo "Lacrei API"
	@echo
	@echo "Available target rules:"
	@echo
	@echo "  build      to build docker image locally"
	@echo "  start      to containers locally using docker compose"
	@echo "  stop       to stop all project running containers"
	@echo "  shell      to enter a shell on running container API"
	@echo "  clean      to clean all project deleting volumes"
	@echo "  tag        to create a git tag and push to repository"
	@echo "  psql       to enter a shell on running container Postgres"
	@echo

VERSION_BUMP ?= minor

version_tag:
	@$(eval VERSION_TAG=v`poetry version --short`)


tag: version_tag
	@poetry version $(VERSION_BUMP)
	@git tag $(VERSION_TAG)
	@git push origin $(VERSION_TAG)


build: version_tag
	@docker build -t lacrei-api:$(VERSION_TAG) . --no-cache


start:
	@cp --update=none contrib/env-sample .env
	@docker compose up


stop:
	@docker compose down --remove-orphans


shell:
	@docker exec -it lacrei_saude_desafio_tecnico-api-1 bash


clean: stop
	@docker volume rm lacrei-saude-desafio-tecnico_pgdata


psql:
	@docker exec -it lacrei-saude-desafio-tecnico-database-1 psql -d app_db -U app_user
