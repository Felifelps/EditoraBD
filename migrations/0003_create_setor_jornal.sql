-- TABELAS: SETOR E JORNAL
CREATE TABLE IF NOT EXISTS setor (
    id_setor INT PRIMARY KEY,
    nome VARCHAR(100),
    descricao TEXT,
    cpf_editor_chefe VARCHAR(11),

    CONSTRAINT fk_setor_editor_chefe
        FOREIGN KEY (cpf_editor_chefe)
        REFERENCES editor_chefe(cpf_editor)
);


CREATE TABLE IF NOT EXISTS jornal (
    nome_jornal VARCHAR(100) PRIMARY KEY,
    cpf_diretor VARCHAR(11),

    CONSTRAINT fk_jornal_diretor
        FOREIGN KEY (cpf_diretor)
        REFERENCES diretor(cpf_diretor)
);