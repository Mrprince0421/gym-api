# Gym Management API

API RESTful para gestão de uma academia de ginástica, desenvolvida para a disciplina de **Programação para a Web II** (UFPI - CSHNB).

## Funcionalidades

- **Autenticação e Autorização (RBAC):** Cadastro e login via JWT com três papéis (`admin`, `trainer` e `member`), além de controle de acesso por função e por objeto.
- **Membros:** Cadastro e consulta de alunos e seus planos.
- **Treinos:** Criação de treinos por instrutores/administradores e consulta por alunos, com cache em Redis (`TTL` de 60s e invalidação explícita após novas inserções).
- **Check-ins:** Registro e histórico de frequência dos membros.
- **Infraestrutura e Segurança:** Pipeline de middlewares (logging, tratamento padronizado de erros, sanitização e validação), migrações com Alembic e balanceamento de carga com Nginx entre réplicas da API.

## Tecnologias Utilizadas

- **Backend:** Python 3.11, FastAPI, SQLAlchemy, Alembic, Pydantic
- **Banco de Dados e Cache:** PostgreSQL 16, Redis 7
- **Infraestrutura:** Docker, Docker Compose, Nginx (Load Balancer)

## Como Executar Localmente

### Pré-requisitos

- [Docker](https://www.docker.com/) e Docker Compose instalados e em execução.

### Passo a passo

1. Clone o repositório e acesse a pasta do projeto:
   ```bash
   git clone <url-do-repositorio>
   cd gym-api
   ```

2. Suba os serviços (banco de dados, Redis, réplicas da API e Nginx):
   ```bash
   docker compose up -d --build
   ```

3. Verifique se a aplicação está respondendo pela porta `8080`:
   ```bash
   curl -i http://localhost:8080/health
   ```

4. Acesse a documentação interativa (Swagger UI) no navegador:
   ```text
   http://localhost:8080/docs
   ```

### Encerrar os containers

```bash
docker compose down
```