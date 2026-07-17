INSERT INTO funcionario (
    cpf, nome, rua, cep, numero, data_nascimento, email, telefone, salario, tipo
) VALUES
    ('00000000000', 'Administrador', NULL, NULL, NULL, '1990-01-01', 'admin@editorabd.com', NULL, 10000.00, 'diretor'),
    ('11111111111', 'Carlos Silva', 'Rua das Flores', '01310100', '120', '1978-03-14', 'carlos.silva@editorabd.com', '11987650001', 9500.00, 'diretor'),
    ('22222222222', 'Fernanda Souza', 'Avenida Paulista', '01311000', '900', '1985-07-22', 'fernanda.souza@editorabd.com', '11987650002', 7200.00, 'editor_chefe'),
    ('33333333333', 'Ricardo Almeida', 'Rua Augusta', '01305000', '45', '1990-11-05', 'ricardo.almeida@editorabd.com', '11987650003', 6800.00, 'editor_chefe'),
    ('44444444444', 'Juliana Costa', 'Rua Oscar Freire', '01426000', '200', '1993-02-18', 'juliana.costa@editorabd.com', '11987650004', 4200.00, 'jornalista'),
    ('55555555555', 'Marcos Pereira', 'Alameda Santos', '01418000', '300', '1996-09-30', 'marcos.pereira@editorabd.com', '11987650005', 4200.00, 'jornalista'),
    ('66666666666', 'Beatriz Lima', 'Rua Haddock Lobo', '01414000', '75', '1998-05-12', 'beatriz.lima@editorabd.com', '11987650006', 4000.00, 'jornalista')
ON CONFLICT (cpf) DO NOTHING;
