-- ============================================================
-- ESQUEMA LOGICO — Sistema de Jornal/Redacao
-- Ordem de criacao respeita as dependencias de FK.
-- ============================================================

-- FUNCIONARIO (superclasse)
CREATE TABLE IF NOT EXISTS funcionario (
    cpf              VARCHAR(11) PRIMARY KEY,
    nome             VARCHAR(100) NOT NULL,
    rua              VARCHAR(100),
    cep              VARCHAR(8),
    numero           VARCHAR(10),
    data_nascimento  DATE,
    email            VARCHAR(100) UNIQUE NOT NULL,
    telefone         VARCHAR(15),
    salario          DECIMAL(10,2),
    idade            INT
);

-- DIRETOR (subtipo de Funcionario)
CREATE TABLE IF NOT EXISTS diretor (
    cpf_diretor          VARCHAR(11) PRIMARY KEY,
    data_inicio_mandato  DATE,

    CONSTRAINT fk_diretor_funcionario
        FOREIGN KEY (cpf_diretor)
        REFERENCES funcionario(cpf)
        ON DELETE CASCADE
);

-- JORNALISTA (subtipo de Funcionario)
CREATE TABLE IF NOT EXISTS jornalista (
    cpf_jornalista  VARCHAR(11) PRIMARY KEY,
    mtb             VARCHAR(20),

    CONSTRAINT fk_jornalista_funcionario
        FOREIGN KEY (cpf_jornalista)
        REFERENCES funcionario(cpf)
        ON DELETE CASCADE
);

-- EDITOR_CHEFE (subtipo de Funcionario)
CREATE TABLE IF NOT EXISTS editor_chefe (
    cpf_editor  VARCHAR(11) PRIMARY KEY,

    CONSTRAINT fk_editor_chefe_funcionario
        FOREIGN KEY (cpf_editor)
        REFERENCES funcionario(cpf)
        ON DELETE CASCADE
);

-- EDITOR_ESPECIALIDADE (atributo multivalorado de Editor_Chefe)
CREATE TABLE IF NOT EXISTS editor_especialidade (
    cpf_editor     VARCHAR(11),
    especialidade  VARCHAR(50),

    PRIMARY KEY (cpf_editor, especialidade),

    CONSTRAINT fk_editor_especialidade_editor_chefe
        FOREIGN KEY (cpf_editor)
        REFERENCES editor_chefe(cpf_editor)
        ON DELETE CASCADE
);

-- JORNAL
CREATE TABLE IF NOT EXISTS jornal (
    nome_jornal   VARCHAR(100) PRIMARY KEY,
    cpf_diretor   VARCHAR(11),

    CONSTRAINT fk_jornal_diretor
        FOREIGN KEY (cpf_diretor)
        REFERENCES diretor(cpf_diretor)
);

-- EDICAO (entidade fraca de Jornal)
CREATE TABLE IF NOT EXISTS edicao (
    nome_jornal    VARCHAR(100),
    numero_edicao  INT,
    data           DATE,

    PRIMARY KEY (nome_jornal, numero_edicao),

    CONSTRAINT fk_edicao_jornal
        FOREIGN KEY (nome_jornal)
        REFERENCES jornal(nome_jornal)
);

-- SETOR
CREATE TABLE IF NOT EXISTS setor (
    id_setor           INT PRIMARY KEY,
    nome               VARCHAR(100),
    descricao          TEXT,
    cpf_editor_chefe   VARCHAR(11) UNIQUE,

    CONSTRAINT fk_setor_editor_chefe
        FOREIGN KEY (cpf_editor_chefe)
        REFERENCES editor_chefe(cpf_editor)
);

-- MATERIA
CREATE TABLE IF NOT EXISTS materia (
    id_materia      SERIAL PRIMARY KEY,
    titulo          VARCHAR(200) NOT NULL,
    subtitulo       VARCHAR(200),
    resumo          TEXT,
    conteudo        TEXT,
    data            DATE,
    status          INT,
    nome_jornal     VARCHAR(100),
    numero_edicao   INT,
    id_setor        INT,

    CONSTRAINT fk_materia_edicao
        FOREIGN KEY (nome_jornal, numero_edicao)
        REFERENCES edicao(nome_jornal, numero_edicao),

    CONSTRAINT fk_materia_setor
        FOREIGN KEY (id_setor)
        REFERENCES setor(id_setor)
);

-- ALOCACAO_JORNALISTA_MATERIA (associativa N:N)
CREATE TABLE IF NOT EXISTS alocacao_jornalista_materia (
    cpf_jornalista  VARCHAR(11),
    id_materia      INT,

    PRIMARY KEY (cpf_jornalista, id_materia),

    CONSTRAINT fk_alocacao_jornalista
        FOREIGN KEY (cpf_jornalista)
        REFERENCES jornalista(cpf_jornalista)
        ON DELETE CASCADE,

    CONSTRAINT fk_alocacao_materia
        FOREIGN KEY (id_materia)
        REFERENCES materia(id_materia)
        ON DELETE CASCADE
);
