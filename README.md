# Editora BD

Projeto Banco de Dados — CRUD de gestão editorial (sem login: acesso direto às páginas).

## Stack

- FastAPI + Jinja2 (templates renderizados no servidor)
- PostgreSQL 15, acessado via **psycopg 3** puro (SQL cru + pool de conexões) — **sem ORM**, ou seja, sem SQLAlchemy nem Django ORM. Todo o acesso a dados fica nas classes `*Repository` em `app/repositories/`.
- Migrações SQL simples (`migrations/*.sql`), aplicadas automaticamente no início da aplicação

## Rodando o projeto

Pré-requisito: Docker e Docker Compose instalados. Não é necessário instalar Python,
uv nem rodar `uv sync` manualmente — tudo isso acontece dentro da imagem, no build do
container (`Dockerfile` roda `uv sync --frozen --no-cache`).

```bash
docker compose up -d --build
```

Isso sobe dois serviços definidos no `docker-compose.yml`:

- `db` — Postgres 15, porta `5432`, usuário `root`, senha `root`, banco `root`.
- `web` — a aplicação FastAPI, porta `8000`, já configurada com a `DATABASE_URL` do
  `db` diretamente no `docker-compose.yml` (sem precisar de `.env`).

Ao iniciar, a aplicação já roda as migrações pendentes automaticamente contra o `db`
(schema + povoamento — ver seção [Povoamento do banco](#povoamento-do-banco) abaixo).

Acesse em http://localhost:8000.

Para derrubar os containers:

```bash
docker compose down
```

Para apagar também os dados do banco (recomeça do zero):

```bash
docker compose down -v
```

## Povoamento do banco

O povoamento é feito **via script DML (`INSERT`)**, não por consumo de API externa. Não
existe um passo manual separado para popular o banco: schema (DDL) e dados (DML) são
tratados como o mesmo mecanismo de migração.

- `migrations/0001_create_tables.sql` — DDL: cria as 10 tabelas do esquema lógico
  (`funcionario`, `diretor`, `jornalista`, `editor_chefe`, `editor_especialidade`,
  `jornal`, `edicao`, `setor`, `materia`, `alocacao_jornalista_materia`), com PKs, FKs
  e constraints.
- `migrations/0002_database_seed.sql` — DML: popula as 10 tabelas, respeitando a ordem
  de dependência das chaves estrangeiras (`funcionario` → subtipos → `jornal` →
  `edicao`/`setor` → `materia` → `alocacao_jornalista_materia`), com no mínimo 50
  tuplas nas tabelas principais (ex.: `funcionario`, `edicao`, `materia`) e 15 nas
  secundárias (ex.: `diretor`, `jornalista`, `editor_chefe`, `jornal`, `setor`,
  `editor_especialidade`, `alocacao_jornalista_materia`).

Esses dois arquivos ficam em `migrations/*.sql` e são aplicados **automaticamente, em
ordem, toda vez que a aplicação sobe** — ver `app/db/migrate.py`, chamado no `lifespan`
de `app/main.py`. Cada arquivo já aplicado é registrado numa única tabela de controle,
`schema_migrations` (criada pelo próprio `migrate.py` se não existir), guardando o nome
do arquivo e o timestamp de quando rodou. Antes de aplicar cada `.sql`, o runner checa
se o nome já está nessa tabela; se estiver, pula — então subir a aplicação de novo
(`docker compose up -d --build`) nunca reaplica nem duplica o que já rodou.

Ou seja: basta iniciar a app que o schema e os dados já ficam em dia, sem comando
manual de migração.

Para adicionar uma nova migração (schema ou dados), crie um arquivo novo em
`migrations/` seguindo o padrão de numeração (`0003_algo.sql`) — ele será aplicado no
próximo start da app.

## Estrutura

```
app/
  main.py          ponto de entrada: cria a FastAPI, roda as migrações no startup
                    (lifespan) e registra os routers
  config.py         leitura de variáveis de ambiente (ex.: DATABASE_URL) via pydantic-settings
  templating.py      configuração do Jinja2 (motor de templates)
  routers/           rotas HTTP — recebem a requisição, chamam o service e devolvem a
                      resposta (JSON ou HTML). Ex.: app/routers/funcionarios.py
  services/           regra de negócio: validações (ex.: CPF duplicado) e orquestração
                      entre repositories, sem falar SQL diretamente
  repositories/        acesso ao banco: todo o SQL cru (psycopg) fica aqui, uma classe
                      *Repository por entidade
  schemas/             modelos Pydantic usados como contrato de entrada/saída da API
                      e para popular os templates
  exceptions/           exceções de domínio (ex.: FuncionarioNaoEncontradoError),
                      traduzidas em respostas HTTP pelos routers
  db/                   pool de conexão (pool.py), dependency do FastAPI para obter uma
                      conexão por requisição (dependencies.py) e o runner de migrações
                      (migrate.py)
  templates/             páginas Jinja2 (HTML), uma pasta por entidade
  static/                 arquivos estáticos (CSS/JS) servidos em /static
migrations/          scripts SQL (DDL + DML), aplicados em ordem no startup da app
```
