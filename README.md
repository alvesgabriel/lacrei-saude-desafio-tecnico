# lacrei-saude-desafio-tecnico
Desafio técnico para voluntariado Backend na Lacrei Saúde

* [API](#api)
    * [Documentação API](#documentação-api)
    * [Endpoints](#endpoints)
        * [Autenticação](#autenticação)
        * [CRUD Usuários](#crud-usuários)
        * [CRUD Profissionais](#crud-profissionais)
        * [CRUD Consultas](#crud-consultas)
            * [Listar Consultas](#listar-consultas)
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

### Documentação API

Para visualizar a documentação via Swagger ou Redoc ao executar o projeto os seguintes endpoints estão disponíveis.

* Swagger: `/api/schema/swagger-ui/`
* Redoc: `/api/schema/redoc/`

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

__POST Exemplo:__
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

#### Autenticação

Após o usuário ser criado ele pode ter acesso aos outros recursos da API fazendo sua autenticação no endpoint `/api/token/`

__Parâmetros:__
| Nome | Tipo |
| --- | --- |
| email | string |
| password | string |

__Authenticação Exemplo:__
```bash
curl -X POST http://localhost:8000/api/token/ \
    -H "Content-Type: application/json" \
    -d '{"email": "alice@example.com", "passowrd": "alice123",}'
```

__Response:__
```json
{
    "acces": <token>,
    "refresh": <token_para_atualizar>
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

__POST Exemplo:__
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

__POST Exemplo:__
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

##### Listar Consultas

O endpoint para listar consultas é o `/api/appointments/`. Ele pode receber os seguintes __query params__ `user_id` e `professional_id`

__GET Exemplo:__
```bash
curl -X GET http://localhost:8000/appointments/?professional_id=1 \
    -H "Authorization: Bearer <token>" \
    -H "Content-Type: application/json"'
```

__Response:__
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "date": "2026-01-01T16:20:00Z",
            "professional": {
                "id": 1,
                "social_name": "",
                "profession": "Médica",
                "email": "alice@example.com",
                "phone": "",
                "address": ""
            }
        }
    ]
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
