-- Senha: admin123 (trocar apos o primeiro acesso)
INSERT INTO funcionario (
    cpf, nome, rua, cep, numero, data_nascimento, email, telefone, salario, senha_hash, tipo
) VALUES (
    '00000000000',
    'Administrador',
    NULL,
    NULL,
    NULL,
    '1990-01-01',
    'admin@editorabd.com',
    NULL,
    10000.00,
    '$2b$12$f50J8ifE5J/4sUqOeYuWg.tS6Mn6e.6a/6Cnus09FiuO6IiT7WP7a',
    'diretor'
)
ON CONFLICT (cpf) DO NOTHING;
