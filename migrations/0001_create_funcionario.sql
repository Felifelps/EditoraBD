-- TABELA: FUNCIONARIO
CREATE TABLE IF NOT EXISTS funcionario (
    cpf VARCHAR(11) PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    rua VARCHAR(100),
    cep VARCHAR(8),
    numero VARCHAR(10),
    data_nascimento DATE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    telefone VARCHAR(15),
    salario DECIMAL(10,2) NOT NULL,
    idade INT
);
