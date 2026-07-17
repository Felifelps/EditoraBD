CREATE TABLE IF NOT EXISTS funcionario (
    cpf             CHAR(11) PRIMARY KEY,
    nome            VARCHAR(120) NOT NULL,
    rua             VARCHAR(120),
    cep             CHAR(8),
    numero          VARCHAR(10),
    data_nascimento DATE NOT NULL,
    email           VARCHAR(120) UNIQUE NOT NULL,
    telefone        VARCHAR(20),
    salario         NUMERIC(10,2) NOT NULL,
    tipo            VARCHAR(20) NOT NULL CHECK (tipo IN ('diretor','editor_chefe','jornalista'))
);
