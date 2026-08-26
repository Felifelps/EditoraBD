# Editora BD

Projeto Banco de Dados — CRUD de gestão editorial, com login de funcionário e tela de
Relatórios como página inicial.

## Integrantes
* **Joran Vinicius Silveira Lage**
* **Matheus Windson Libório Araújo**
* **Felipe dos Santos Ferreira**
* **Leonardo Sabino Pereira**
  
## Stack

- FastAPI + Jinja2 (templates renderizados no servidor)
- PostgreSQL 15, acessado via **psycopg 3** puro (SQL cru + pool de conexões) — **sem ORM**, ou seja, sem SQLAlchemy nem Django ORM. Todo o acesso a dados fica nas classes `*Repository` em `app/repositories/`.
- Migrações SQL simples (`migrations/*.sql`), aplicadas automaticamente no início da aplicação
- Bootstrap 5 (via CDN) + design tokens próprios em `app/static/css/app.css` (cores, raio de borda, sombra) reaproveitados em toda a aplicação — sem framework de componentes adicional
- [Chart.js](https://www.chartjs.org/) (via CDN, só na tela de Relatórios) para os gráficos do dashboard

## Rodando o projeto

Pré-requisito: Docker e Docker Compose instalados.

```bash
docker compose up -d --build
```

Isso sobe dois serviços definidos no `docker-compose.yml`:

- `db` — Postgres 15, porta `5432`, usuário `root`, senha `root`, banco `root`.
- `web` — a aplicação FastAPI, porta `8000`, já configurada com a `DATABASE_URL` do
  `db` diretamente no `docker-compose.yml` (sem precisar de `.env`).

Não existe um serviço de frontend separado: as telas (HTML) são renderizadas no
próprio servidor pelo FastAPI via Jinja2, então o frontend é servido na **mesma porta
`8000`** do backend.

Ao iniciar, a aplicação já roda as migrações pendentes automaticamente contra o `db`.

Acesse em http://localhost:8000.
Para teste usar email: "teste@editorabd.com" e senha: "senha123"

Para derrubar os containers:

```bash
docker compose down
```

Para apagar também os dados do banco (recomeça do zero):

```bash
docker compose down -v
```

## Login

A aplicação exige login de funcionário para acessar qualquer página — tentar abrir
`http://localhost:8000/` (ou qualquer rota interna) sem estar autenticado redireciona
automaticamente para `http://localhost:8000/login`.

**Autenticação:** e-mail + senha do funcionário. A senha é validada no backend contra
um hash salgado (PBKDF2-HMAC-SHA256, `app/security.py`) guardado na nova coluna
`funcionario.senha_hash` — nunca em texto puro. A sessão é mantida por um cookie
assinado (`SessionMiddleware` do Starlette, chave configurável via a variável de
ambiente `SESSION_SECRET`); "Sair" no cabeçalho encerra a sessão.

**Usuário de teste** (criado automaticamente pela migration
`0004_add_login_funcionario.sql`, disponível logo após `docker compose up`, sem
nenhum passo manual):

```text
E-mail: teste@editorabd.com
Senha:  senha123
```

Após o login, o usuário é direcionado direto para a tela de **Relatórios**, que passa
a ser a página inicial do sistema. As demais áreas (Funcionários, Jornais, Edições,
Setores, Matérias) continuam acessíveis pelo menu no cabeçalho.

## Povoamento do banco

O povoamento é feito **via script DML (`INSERT`)**. Não
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
- `migrations/0003_create_views.sql` — DDL: cria as 5 Views SQL usadas na tela de
  Relatórios (ver seção [Views SQL e Relatórios](#views-sql-e-relatórios)).
- `migrations/0004_add_login_funcionario.sql` — DDL + DML: adiciona a coluna
  `funcionario.senha_hash` e cria o funcionário de teste usado no login (ver seção
  [Login](#login)).

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
`migrations/` seguindo o padrão de numeração (`0004_algo.sql`) — ele será aplicado no
próximo start da app.

## Views SQL e Relatórios

`migrations/0003_create_views.sql` cria 5 Views que unem dados de 3+ tabelas para
simplificar as consultas usadas nos relatórios:

| View | Tabelas envolvidas | Finalidade |
|---|---|---|
| `vw_resumo_edicoes_jornal` | `jornal`, `diretor`, `funcionario`, `edicao` | Total de edições e data da última edição de cada jornal, com o nome do diretor responsável. |
| `vw_carga_materias_jornalista` | `jornalista`, `funcionario`, `alocacao_jornalista_materia`, `materia` | Quantidade de matérias por jornalista, já separadas por status (aprovadas/reprovadas/em andamento). |
| `vw_setores_editores` | `setor`, `editor_chefe`, `funcionario`, `editor_especialidade` | Cada setor com o nome do editor-chefe responsável e suas especialidades agregadas. |
| `vw_funcionarios_detalhes` | `funcionario`, `diretor`, `jornalista`, `editor_chefe` | Todos os funcionários com o cargo (Diretor/Jornalista/Editor-Chefe) resolvido dinamicamente a partir da herança. |
| `vw_materias_completas` | `materia`, `setor`, `edicao`, `alocacao_jornalista_materia`, `jornalista`, `funcionario` | Catálogo de matérias com setor, edição/jornal, status por extenso e os autores agregados. |

Essas Views são consultadas por `app/repositories/relatorios.py` e exibidas na tela
`GET /relatorios` (`app/routers/relatorios.py` + `app/templates/relatorios/list.html`),
que é a **página inicial** do sistema após o login (também acessível a qualquer
momento pelo link "Relatorios", primeiro item do menu no cabeçalho).

### Dashboard

A tela é um dashboard, não uma lista de tabelas empilhadas:

- **4 indicadores** no topo (Jornais, Edições, Jornalistas, Matérias) — somas/contagens
  calculadas a partir dos próprios dados das Views, sem consulta extra.
- **4 gráficos** (biblioteca [Chart.js](https://www.chartjs.org/), via CDN — a única
  adicionada; nenhuma dependência Python nova), um para cada View além do catálogo de
  matérias:
  - *Edições por jornal* — ranking em barras horizontais (`vw_resumo_edicoes_jornal`);
    o tooltip de cada barra mostra o diretor e a data da última edição.
  - *Carga de matérias por jornalista* — ranking em barras horizontais **empilhadas**
    por status (aprovadas/em andamento/reprovadas), usando as colunas já agregadas de
    `vw_carga_materias_jornalista` — sem recalcular nada no frontend.

  Os dois rankings mostram só o **Top 10** no gráfico (com mais categorias o gráfico
  fica ilegível) — a tabela logo abaixo continua com a lista completa.
  - *Especialidades dos editores-chefe* — barras horizontais com quantos setores cada
    especialidade cobre, derivado do campo `especialidades` (agregado) de
    `vw_setores_editores`.
  - *Funcionários por cargo* — gráfico de rosca com a composição
    Diretor/Jornalista/Editor-Chefe/sem cargo, a partir de `vw_funcionarios_detalhes`.
- Cada gráfico é acompanhado de uma **tabela complementar** com os valores exatos, e o
  catálogo de matérias (`vw_materias_completas`, a View mais extensa) permanece só como
  tabela — é a camada de consulta detalhada do dashboard.
- Cores dos gráficos reaproveitam as mesmas variáveis CSS (`--cor-primaria`,
  `--cor-sucesso`, `--cor-aviso`, `--cor-perigo`, ...) já usadas nos badges de status do
  resto da aplicação, lidas em tempo de execução via `getComputedStyle`.

O layout usa um grid responsivo (`.relatorios-grid` em `app/static/css/app.css`): os
quatro primeiros relatórios ficam em pares lado a lado (uma coluna só em telas
menores) e o catálogo de matérias — o mais extenso — ocupa a largura inteira embaixo.
Cada card tem sua própria área de rolagem vertical (com cabeçalho de tabela fixo) para
não esticar a página, além do scroll horizontal já existente por tabela. Cada seção
trata individualmente os estados de carregando (spinner no botão "Atualizar"), erro
(mensagem amigável, sem stack trace) e sem dados — uma falha ou ausência de dados numa
View não derruba as demais.

## Esquema Conceitual

```mermaid
erDiagram
    FUNCIONARIO ||--o| DIRETOR : especializa
    FUNCIONARIO ||--o| JORNALISTA : especializa
    JORNALISTA ||--o| EDITOR_CHEFE : especializa
    EDITOR_CHEFE ||--o{ EDITOR_ESPECIALIDADE : possui
    DIRETOR ||--o{ JORNAL : administra
    JORNAL ||--o{ EDICAO : publica
    EDITOR_CHEFE |o--o| SETOR : chefia
    EDICAO ||--o{ MATERIA : contem
    SETOR ||--o{ MATERIA : classifica
    JORNALISTA ||--o{ ALOCACAO_JORNALISTA_MATERIA : escreve
    MATERIA ||--o{ ALOCACAO_JORNALISTA_MATERIA : recebe_autoria

    FUNCIONARIO {
        varchar cpf PK
        varchar nome
        date data_nascimento
        varchar email UK
        decimal salario
        varchar senha_hash
    }
    DIRETOR {
        varchar cpf_diretor PK, FK
        date data_inicio_mandato
    }
    JORNALISTA {
        varchar cpf_jornalista PK, FK
        varchar mtb
    }
    EDITOR_CHEFE {
        varchar cpf_editor PK, FK
    }
    EDITOR_ESPECIALIDADE {
        varchar cpf_editor PK, FK
        varchar especialidade PK
    }
    JORNAL {
        varchar nome_jornal PK
        varchar cpf_diretor FK
    }
    EDICAO {
        varchar nome_jornal PK, FK
        int numero_edicao PK
        date data
    }
    SETOR {
        int id_setor PK
        varchar nome
        text descricao
        varchar cpf_editor_chefe FK, UK
    }
    MATERIA {
        int id_materia PK
        varchar titulo
        int status
        varchar nome_jornal FK
        int numero_edicao FK
        int id_setor FK
    }
    ALOCACAO_JORNALISTA_MATERIA {
        varchar cpf_jornalista PK, FK
        int id_materia PK, FK
    }
```

Importante: `Editor_Chefe` especializa `Jornalista` (não `Funcionario` diretamente) —
todo editor-chefe é, por definição, um jornalista, o que permite que ele apareça em
`alocacao_jornalista_materia` como autor. Ver `migrations/0001_create_tables.sql`,
constraint `fk_editor_chefe_jornalista`.

> Os arquivos `Diagrama Lógico UML.pdf` e `Dicionário de Dados.pdf`, na raiz do
> repositório, foram produzidos na entrega anterior e ainda descrevem `Editor_Chefe`
> como especialização direta de `Funcionario` — ficaram desatualizados após a correção
> acima. O diagrama e o dicionário desta seção do README refletem o schema atual
> (`migrations/0001_create_tables.sql`) e devem ser tratados como a fonte da verdade
> até que os PDFs sejam regerados.

## Dicionário de Dados

### Funcionario (superclasse)

| Atributo | Tipo | Restrições | Descrição |
|---|---|---|---|
| cpf | VARCHAR(11) | PK, NOT NULL | CPF do funcionário (apenas números). |
| nome | VARCHAR(100) | NOT NULL | Nome completo. |
| rua | VARCHAR(100) | - | Logradouro do endereço. |
| cep | VARCHAR(8) | - | CEP (apenas números). |
| numero | VARCHAR(10) | - | Número/complemento do endereço. |
| data_nascimento | DATE | CHECK ≤ data atual | Data de nascimento. |
| email | VARCHAR(100) | UNIQUE, NOT NULL | E-mail de contato. |
| telefone | VARCHAR(15) | - | Telefone com DDD. |
| salario | DECIMAL(10,2) | CHECK ≥ 0 | Remuneração bruta mensal. |
| idade | INT | - | Atributo derivado (não populado automaticamente hoje). |
| senha_hash | VARCHAR(255) | - | Hash salgado (PBKDF2-HMAC-SHA256) da senha de login; nulo para funcionários sem acesso ao sistema. Ver seção [Login](#login). |

### Diretor (especializa Funcionario)

| Atributo | Tipo | Restrições | Descrição |
|---|---|---|---|
| cpf_diretor | VARCHAR(11) | PK, FK → funcionario.cpf | Identifica o diretor. |
| data_inicio_mandato | DATE | CHECK ≤ data atual | Início do mandato. |

### Jornalista (especializa Funcionario)

| Atributo | Tipo | Restrições | Descrição |
|---|---|---|---|
| cpf_jornalista | VARCHAR(11) | PK, FK → funcionario.cpf | Identifica o jornalista. |
| mtb | VARCHAR(20) | - | Registro profissional (MTb). |

### Editor_Chefe (especializa Jornalista)

| Atributo | Tipo | Restrições | Descrição |
|---|---|---|---|
| cpf_editor | VARCHAR(11) | PK, FK → jornalista.cpf_jornalista | Todo editor-chefe é um jornalista. |

### Editor_Especialidade (atributo multivalorado de Editor_Chefe)

| Atributo | Tipo | Restrições | Descrição |
|---|---|---|---|
| cpf_editor | VARCHAR(11) | PK, FK → editor_chefe.cpf_editor | Editor-chefe associado. |
| especialidade | VARCHAR(50) | PK | Área de especialização (ex.: Política, Economia). |

### Jornal

| Atributo | Tipo | Restrições | Descrição |
|---|---|---|---|
| nome_jornal | VARCHAR(100) | PK | Nome do veículo. |
| cpf_diretor | VARCHAR(11) | FK → diretor.cpf_diretor | Diretor responsável (opcional). |

### Edicao (entidade fraca de Jornal)

| Atributo | Tipo | Restrições | Descrição |
|---|---|---|---|
| nome_jornal | VARCHAR(100) | PK, FK → jornal.nome_jornal | Jornal ao qual pertence. |
| numero_edicao | INT | PK | Número sequencial da edição. |
| data | DATE | - | Data de circulação. |

### Setor

| Atributo | Tipo | Restrições | Descrição |
|---|---|---|---|
| id_setor | INT | PK | Identificador da editoria. |
| nome | VARCHAR(100) | - | Nome da editoria. |
| descricao | TEXT | - | Escopo de cobertura. |
| cpf_editor_chefe | VARCHAR(11) | UNIQUE, FK → editor_chefe.cpf_editor | Editor-chefe responsável (1:1, opcional). |

### Materia

| Atributo | Tipo | Restrições | Descrição |
|---|---|---|---|
| id_materia | SERIAL | PK | Identificador autoincremental. |
| titulo | VARCHAR(200) | - | Manchete. |
| subtitulo | VARCHAR(200) | - | Linha fina. |
| resumo | TEXT | - | Lead/síntese. |
| conteudo | TEXT | - | Texto integral. |
| data | DATE | - | Data de elaboração/publicação. |
| status | INT | NOT NULL, DEFAULT 2, CHECK IN (0,1,2) | Etapa editorial: `0` = Reprovada, `1` = Aprovada, `2` = Em Andamento. |
| nome_jornal | VARCHAR(100) | FK (composta c/ numero_edicao) → edicao | Edição de veiculação (opcional). |
| numero_edicao | INT | FK (composta) → edicao | Edição de veiculação (opcional). |
| id_setor | INT | FK → setor.id_setor | Editoria responsável (opcional). |

### Alocacao_Jornalista_Materia (associativa N:N)

| Atributo | Tipo | Restrições | Descrição |
|---|---|---|---|
| cpf_jornalista | VARCHAR(11) | PK, FK → jornalista.cpf_jornalista | Jornalista autor/coautor. |
| id_materia | INT | PK, FK → materia.id_materia | Matéria correspondente. |

## Trigger

`migrations/0005_trigger_historico_status_materia.sql` cria a única trigger do banco,
com foco em **auditoria**: registrar toda mudança de status de uma matéria, sem
depender de nenhuma lógica no backend — funciona mesmo que o `UPDATE` seja feito
direto no banco, fora da aplicação.

| | |
|---|---|
| Nome | `trg_historico_status_materia` |
| Dispara em | `AFTER UPDATE OF status ON materia`, `FOR EACH ROW` |
| Função associada | `fn_registrar_historico_status_materia()` |
| Tabela de auditoria | `historico_status_materia` (`id_materia`, `status_anterior`, `status_novo`, `alterado_em`) |

**Regra de negócio:** sempre que `materia.status` muda de valor (comparação
`OLD.status IS DISTINCT FROM NEW.status`, para não gravar nada em updates que não
afetam o status), a trigger insere uma linha em `historico_status_materia` com o
status anterior, o novo status e o timestamp da alteração. Isso existe para dar
rastreabilidade ao fluxo editorial (quem aprovou/reprovou o quê e quando fica
registrado de forma imutável, independente de quem ou o quê alterou a matéria),
sem exigir nenhuma alteração no código da aplicação para ser mantido.

### Como testar

**Via UI** — aprovando/reprovando uma matéria:

1. Acesse `/materias`, abra uma matéria existente e clique em "Editar".
2. Troque o campo "Status" (ex.: de "Em Andamento" para "Aprovada" ou "Reprovada") e
   salve.
3. Confirme que a trigger disparou consultando a tabela de auditoria (via SQL, abaixo)
   — deve existir uma linha nova para aquele `id_materia`.

**Via SQL direto** — sem passar pela aplicação:

```bash
docker compose exec db psql -U root -d root
```

```sql
-- estado antes: quantas linhas de historico a materia 1 ja tem
SELECT * FROM historico_status_materia WHERE id_materia = 1 ORDER BY alterado_em DESC;

-- dispara a trigger com um UPDATE direto no banco (troque o valor para algo
-- diferente do status atual da materia)
UPDATE materia SET status = 1 WHERE id_materia = 1;

-- confirma que uma nova linha foi registrada automaticamente
SELECT * FROM historico_status_materia WHERE id_materia = 1 ORDER BY alterado_em DESC;
```

Rodar o mesmo `UPDATE` de novo com o mesmo valor de `status` (sem mudança real) não
gera uma nova linha — a trigger só registra transições efetivas de status.

## Testes

Testes de integração ponta a ponta (`tests/test_smoke.py`, com `pytest` + o
`TestClient` do FastAPI) cobrem: login com credenciais válidas/inválidas, bloqueio de
acesso sem autenticação, logout (e bloqueio de acesso após ele), carregamento das
páginas principais, CRUD completo de uma entidade, o dashboard de Relatórios exibindo
as 5 Views (gráficos + tabelas), que os números embutidos nos gráficos batem com uma
consulta direta às Views, e o tratamento de erro para uma referência inválida (FK). Não
usam mocks — rodam contra um Postgres de verdade.

Pré-requisito: o banco acessível (`docker compose up -d db`, ou a stack completa).

```bash
uv run pytest
```

## Estrutura

```
app/
  main.py
  config.py
  templating.py
  routers/
  services/
  repositories/
  schemas/
  exceptions/
  db/
  templates/
  static/
migrations/
```

| Caminho | Responsabilidade |
|---|---|
| `app/main.py` | Ponto de entrada: cria a FastAPI, roda as migrações no startup (`lifespan`), registra o `SessionMiddleware`, os routers e os exception handlers globais |
| `app/config.py` | Leitura de variáveis de ambiente (ex.: `DATABASE_URL`, `SESSION_SECRET`) via pydantic-settings |
| `app/templating.py` | Configuração do Jinja2 (motor de templates) |
| `app/security.py` | Hash e verificação de senha (PBKDF2-HMAC-SHA256) usados no login |
| `app/routers/` | Rotas HTTP — recebem a requisição, chamam o service e devolvem a resposta (JSON ou HTML). Ex.: `app/routers/funcionarios.py` |
| `app/services/` | Regra de negócio: validações (ex.: CPF duplicado) e orquestração entre repositories, sem falar SQL diretamente |
| `app/repositories/` | Acesso ao banco: todo o SQL cru (psycopg) fica aqui, uma classe `*Repository` por entidade |
| `app/schemas/` | Modelos Pydantic usados como contrato de entrada/saída da API e para popular os templates |
| `app/exceptions/` | Exceções de domínio (ex.: `FuncionarioNaoEncontradoError`), traduzidas em respostas HTTP pelos routers |
| `app/db/` | Pool de conexão (`pool.py`), dependency do FastAPI para obter uma conexão por requisição (`dependencies.py`) e o runner de migrações (`migrate.py`) |
| `app/templates/` | Páginas Jinja2 (HTML), uma pasta por entidade |
| `app/static/` | Arquivos estáticos (CSS/JS) servidos em `/static` |
| `migrations/` | Scripts SQL (DDL + DML), aplicados em ordem no startup da app |
