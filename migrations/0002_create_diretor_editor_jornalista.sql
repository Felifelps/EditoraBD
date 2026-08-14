-- Tabelas filhas: diretor, editor_chefe (+ editor_especialidade) e jornalista.
CREATE TABLE IF NOT EXISTS diretor (
    cpf_diretor VARCHAR(11) PRIMARY KEY,
    data_inicio_mandato DATE,

    CONSTRAINT fk_diretor_funcionario
        FOREIGN KEY (cpf_diretor)
        REFERENCES funcionario(cpf)
);

CREATE TABLE IF NOT EXISTS editor_chefe (
    cpf_editor VARCHAR(11) PRIMARY KEY,

    CONSTRAINT fk_editor_chefe_funcionario
        FOREIGN KEY (cpf_editor)
        REFERENCES funcionario(cpf)
);

CREATE TABLE IF NOT EXISTS jornalista (
    cpf_jornalista VARCHAR(11) PRIMARY KEY,
    mtb VARCHAR(20),

    CONSTRAINT fk_jornalista_funcionario
        FOREIGN KEY (cpf_jornalista)
        REFERENCES funcionario(cpf)
);

CREATE TABLE IF NOT EXISTS editor_especialidade (
    cpf_editor VARCHAR(11),
    especialidade VARCHAR(50),

    PRIMARY KEY (cpf_editor, especialidade),

    CONSTRAINT fk_editor_especialidade
        FOREIGN KEY (cpf_editor)
        REFERENCES editor_chefe(cpf_editor)
);