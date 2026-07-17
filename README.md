# Editora BD

Projeto Banco de Dados — CRUD de gestão editorial (sem login: acesso direto às páginas).

## Stack

- FastAPI + Jinja2 (templates renderizados no servidor)
- PostgreSQL via psycopg (pool de conexões)
- Migrações SQL simples, aplicadas automaticamente no início da aplicação

## Rodando com Docker (recomendado)

Pré-requisito: Docker e Docker Compose instalados.

```bash
docker compose up
```

Isso sobe dois serviços: `web` (a aplicação, porta 8000) e `db` (Postgres, porta 5432).
Ao iniciar, a aplicação já roda as migrações pendentes automaticamente contra o `db`.

Acesse em http://localhost:8000.

Para derrubar os containers:

```bash
docker compose down
```

Para apagar também os dados do banco (recomeça do zero):

```bash
docker compose down -v
```

## Rodando localmente (sem Docker)

Pré-requisitos: Python 3.12+, [uv](https://docs.astral.sh/uv/) e um Postgres acessível.

1. Suba um Postgres (pode usar só o serviço `db` do compose):

   ```bash
   docker compose up db
   ```

2. Instale as dependências:

   ```bash
   uv sync
   ```

3. (Opcional) configure a conexão criando um `.env` na raiz — por padrão a app usa
   `postgresql://root:root@localhost:5432/root`, que já bate com o `db` do compose:

   ```
   DATABASE_URL=postgresql://usuario:senha@localhost:5432/banco
   ```

4. Rode a aplicação:

   ```bash
   uv run uvicorn app.main:app --reload
   ```

Acesse em http://localhost:8000.

## Migrações

As migrações ficam em `migrations/*.sql` e são aplicadas **automaticamente, em ordem,
toda vez que a aplicação sobe** (ver `app/db/migrate.py`, chamado no `lifespan` de
`app/main.py`). Cada arquivo já aplicado é registrado na tabela `schema_migrations`,
então rodar a app de novo não reaplica o que já rodou.

Ou seja: não existe um comando manual separado para migrar — basta iniciar a app
(`docker compose up` ou `uv run uvicorn app.main:app`) que o schema já fica em dia.

Para adicionar uma nova migração, crie um arquivo novo em `migrations/` seguindo o
padrão de numeração (`0006_algo.sql`) — ele será aplicado no próximo start da app.

## Estrutura

```
app/
  routers/        rotas HTTP (ex.: app/routers/funcionarios.py)
  repositories/    acesso ao banco (SQL)
  schemas/         modelos Pydantic
  templates/       páginas Jinja2 (HTML)
  db/              pool de conexão e runner de migrações
migrations/        scripts SQL, aplicados em ordem
```

## Funcionalidade de exemplo: Funcionários

- `GET /funcionarios` — lista os funcionários cadastrados
- `GET /funcionarios/novo` — formulário de cadastro
- `POST /funcionarios/novo` — cria um novo funcionário

Use esse CRUD como modelo para os demais (setores, jornais, matérias, edições).
