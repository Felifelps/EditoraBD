-- ============================================================
-- LOGIN — adiciona suporte a autenticacao de Funcionario
-- ============================================================

-- Hash da senha (PBKDF2-HMAC-SHA256, salt$hash) — ver app/security.py.
-- Nulo para funcionarios sem acesso ao sistema (a maioria do seed atual).
ALTER TABLE funcionario ADD COLUMN IF NOT EXISTS senha_hash VARCHAR(255);

-- Funcionario de teste para demonstrar o login (credenciais no README):
-- email: teste@editorabd.com | senha: senha123
INSERT INTO funcionario
    (cpf, nome, data_nascimento, email, salario, senha_hash)
VALUES
    (
        '00000000001',
        'Usuário de Teste',
        '1990-01-01',
        'teste@editorabd.com',
        0,
        '5528dfb110875818235652fbd18e7310$5276accc0c87c2ffe44c2097a4df1dceac0a3584b2e5a8b2437a7334e2f98321'
    )
ON CONFLICT (cpf) DO NOTHING;
