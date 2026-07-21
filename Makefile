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
	@echo "  psql       to enter a shell on running container Postgres"
	@echo


build:
	@docker build -t lacrei-api . --no-cache


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
