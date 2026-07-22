# lacrei-saude-desafio-tecnico
Desafio técnico para voluntariado Backend na Lacrei Saúde

* [API](#api)
    * [Endpoints](#endpoints)
        * [CRUD Usuários](#crud-usuários)
        * [CRUD Profissionais](#crud-profissionais)
        * [CRUD Consultas](#crud-consultas)
* [Execução do Código](#execução-do-código)
    * [Comandos](#comandos)
        * [Ajuda](#ajuda)
        * [Build](#build)
        * [Execução da API](#execução-da-api)
        * [Parar API e servicos](#parar-api-e-servicos)
        * [Limpar](#limpar)
        * [Tag](#tag)

## API

A API REST foi feita em [Django Rest Framework](https://www.django-rest-framework.org/). O código para a API está no diretório `./lacrei/`

### Endpoints

#### CRUD Usuários

__Endpoints:__
* POST `/users/`
* GET `/users/`
* GET `/users/<user_id>`
* PUT `/users/<user_id>`
* PATCH `/users/<user_id>`
* DELETE `/users/<user_id>`

__Parâmetros:__
| Nome | Tipo |
| --- | --- |
| id | integer |
| email | string |
| password | string |

__POST Example:__
```bash
curl -X POST http://localhost:8000/users/ \
    -H "Content-Type: application/json" \
    -d '{"email": "alice@example.com", "password": "alice123"}'
```

__Response:__
```json
{
    "id": 1,
    "email": "alice3@example.com"
}
```

#### CRUD Profissionais

__Endpoints:__
* POST `/professionais/`
* GET `/professionais/`
* GET `/professionais/<user_id>`
* PUT `/professionais/<user_id>`
* PATCH `/professionais/<user_id>`
* DELETE `/professionais/<user_id>`

__Parâmetros:__
| Nome | Tipo |
| --- | --- |
| id | integer |
| email | string |
| password | string |
| social_name | string |
| profession | string |
| address | string |
| email | string |
| phone | string |

__POST Example:__
```bash
curl -X POST http://localhost:8000/professionals/ \
    -H "Authorization: Bearer <token>" \
    -H "Content-Type: application/json" \
    -d '{"social_name": "Alice", "profession": "Medica", "address": "Rua das Flores, 120", "email": "alice@example.com", "phone": "+5521987654321",}'
```

__Response:__
```json
{
    "id": 1,
    "social_name": "Alice",
    "profession": "Medica",
    "address": "Rua das Flores, 120",
    "email": "alice@example.com",
    "phone": "+5521987654321"
}
```

#### CRUD Consultas

__Endpoints:__
* POST `/appointments/`
* GET `/appointments/`
* GET `/appointments/<user_id>`
* PUT `/appointments/<user_id>`
* PATCH `/appointments/<user_id>`
* DELETE `/appointments/<user_id>`

__Parâmetros:__
| Nome | Tipo |
| --- | --- |
| id | integer |
| date | date |
| professional | object |
| professional_id | integer |

__POST Example:__
```bash
curl -X POST http://localhost:8000/appointments/ \
    -H "Authorization: Bearer <token>" \
    -H "Content-Type: application/json" \
    -d '{"date": "2026-01-01 16:20:00", "professional_id": 1}'
```

__Response:__
```json
{
    "id": 1,
    "date": "2026-01-01T16:20:00Z",
    "professional": {
        "id": 1,
        "social_name": "Alice",
        "profession": "Medica",
        "address": "Rua das Flores, 120",
        "email": "alice@example.com",
        "phone": "+5521987654321"
    }
}
```

## Execução do Código
Foram desenvolvidas algumas configurações para simplificar a execução do código. `Dockerfile` para criar imagem e versionamento do sistema. `docker-compose.yaml` para subir os sitemas os serviços necessários para executar a API. `Makefile` para centralizar execução dos comandos.

### Comandos

#### Ajuda
Comando para ajuda no `make`
```shell
make help
```

#### Build
Comando para fazer o build da imagem com base no `Dockerfile`
```shell
make build
```

#### Execução da API
Comando para subir os serviços junto com a API
```shell
make start
```

#### Parar API e servicos
Comando para parar os serviços junto com a API
```shell
make stop
```

#### Limpar
Comando para limpar os serviços junto com a API
```shell
make clean
```

#### Tag
Comando para criar uma tag do git e atuliza-la no repositório remoto.
```shell
make tag
```

Ele por padrão atualiza a versão `minor` mas ele pode receber um valor `VERSION_BUMP=(major|minor|patch)`

__Exemplo para atualizar a versão major:__
```shell
make tag VERSION_BUMP=major
```
