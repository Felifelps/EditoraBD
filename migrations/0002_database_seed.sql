-- ============================================================
-- POVOAMENTO DO BANCO — Sistema de Jornal/Redacao
-- Ordem respeita as dependencias de FK (ver README/spec).
-- ============================================================

-- ============================================================
-- POVOAMENTO: FUNCIONARIO
-- Quantidade: 60 tuplas
-- ============================================================

INSERT INTO funcionario
    (cpf, nome, rua, cep, numero, data_nascimento, email, telefone, salario, idade)
VALUES
    ('10000000001', 'Ana Beatriz Silva', 'Rua das Flores', '50000001', '101', '1985-02-14', 'ana.silva@email.com', '81990000001', 4500.00, 41),
    ('10000000002', 'Bruno Henrique Santos', 'Rua do Sol', '50000002', '102', '1988-05-21', 'bruno.santos@email.com', '81990000002', 5200.00, 38),
    ('10000000003', 'Carla Mendes Oliveira', 'Rua Central', '50000003', '103', '1990-07-10', 'carla.oliveira@email.com', '81990000003', 4800.00, 36),
    ('10000000004', 'Daniel Pereira Costa', 'Rua Nova', '50000004', '104', '1982-11-03', 'daniel.costa@email.com', '81990000004', 6100.00, 43),
    ('10000000005', 'Eduarda Martins Souza', 'Rua da Paz', '50000005', '105', '1992-01-18', 'eduarda.souza@email.com', '81990000005', 3900.00, 34),
    ('10000000006', 'Felipe Almeida Rocha', 'Rua Boa Vista', '50000006', '106', '1987-03-27', 'felipe.rocha@email.com', '81990000006', 4700.00, 39),
    ('10000000007', 'Gabriela Ferreira Lima', 'Rua Verde', '50000007', '107', '1995-06-12', 'gabriela.lima@email.com', '81990000007', 3600.00, 31),
    ('10000000008', 'Henrique Barbosa Alves', 'Rua do Comercio', '50000008', '108', '1980-09-25', 'henrique.alves@email.com', '81990000008', 6800.00, 45),
    ('10000000009', 'Isabela Carvalho Melo', 'Rua Principal', '50000009', '109', '1993-12-08', 'isabela.melo@email.com', '81990000009', 4100.00, 32),
    ('10000000010', 'Joao Victor Ribeiro', 'Rua Esperanca', '50000010', '110', '1989-04-16', 'joao.ribeiro@email.com', '81990000010', 5000.00, 37),
    ('10000000011', 'Julia Cristina Nunes', 'Rua das Acacias', '50000011', '111', '1991-08-22', 'julia.nunes@email.com', '81990000011', 4300.00, 35),
    ('10000000012', 'Lucas Gabriel Teixeira', 'Rua do Parque', '50000012', '112', '1986-10-30', 'lucas.teixeira@email.com', '81990000012', 5500.00, 39),
    ('10000000013', 'Mariana Duarte Campos', 'Rua das Palmeiras', '50000013', '113', '1994-02-05', 'mariana.campos@email.com', '81990000013', 3800.00, 32),
    ('10000000014', 'Nicolas Araujo Freitas', 'Rua do Lago', '50000014', '114', '1983-06-19', 'nicolas.freitas@email.com', '81990000014', 6200.00, 43),
    ('10000000015', 'Olivia Ramos Batista', 'Rua das Palmeiras', '50000015', '115', '1996-09-11', 'olivia.batista@email.com', '81990000015', 3500.00, 29),
    ('10000000016', 'Paulo Roberto Dias', 'Rua do Norte', '50000016', '116', '1981-12-24', 'paulo.dias@email.com', '81990000016', 5900.00, 44),
    ('10000000017', 'Rafaela Gomes Moura', 'Rua da Amizade', '50000017', '117', '1990-03-09', 'rafaela.moura@email.com', '81990000017', 4600.00, 36),
    ('10000000018', 'Ricardo Fernandes Reis', 'Rua da Estacao', '50000018', '118', '1985-07-28', 'ricardo.reis@email.com', '81990000018', 5100.00, 41),
    ('10000000019', 'Sabrina Moreira Lopes', 'Rua do Campo', '50000019', '119', '1997-01-13', 'sabrina.lopes@email.com', '81990000019', 3400.00, 29),
    ('10000000020', 'Thiago Cavalcante Barros', 'Rua do Mercado', '50000020', '120', '1984-05-06', 'thiago.barros@email.com', '81990000020', 5700.00, 42),
    ('10000000021', 'Amanda Cristina Maia', 'Rua do Bosque', '50000021', '121', '1992-11-17', 'amanda.maia@email.com', '81990000021', 4000.00, 33),
    ('10000000022', 'Anderson Martins Pinto', 'Rua da Serra', '50000022', '122', '1987-02-26', 'anderson.pinto@email.com', '81990000022', 5300.00, 39),
    ('10000000023', 'Beatriz Fonseca Cardoso', 'Rua das Flores', '50000023', '123', '1995-04-15', 'beatriz.cardoso@email.com', '81990000023', 3700.00, 31),
    ('10000000024', 'Caio Henrique Moraes', 'Rua do Porto', '50000024', '124', '1989-09-07', 'caio.moraes@email.com', '81990000024', 4900.00, 36),
    ('10000000025', 'Camila Rodrigues Sales', 'Rua da Praia', '50000025', '125', '1993-12-21', 'camila.sales@email.com', '81990000025', 4200.00, 32),
    ('10000000026', 'Diego Martins Cunha', 'Rua do Centro', '50000026', '126', '1982-08-14', 'diego.cunha@email.com', '81990000026', 6300.00, 43),
    ('10000000027', 'Elisa Monteiro Ramos', 'Rua do Jardim', '50000027', '127', '1991-05-23', 'elisa.ramos@email.com', '81990000027', 4400.00, 35),
    ('10000000028', 'Fernando Castro Vieira', 'Rua das Flores', '50000028', '128', '1986-01-31', 'fernando.vieira@email.com', '81990000028', 5600.00, 40),
    ('10000000029', 'Giovana Correia Silva', 'Rua do Carmo', '50000029', '129', '1996-07-04', 'giovana.silva@email.com', '81990000029', 3600.00, 30),
    ('10000000030', 'Gustavo Martins Leite', 'Rua da Matriz', '50000030', '130', '1983-10-12', 'gustavo.leite@email.com', '81990000030', 6000.00, 42),
    ('10000000031', 'Helena Souza Lima', 'Rua do Sol', '50000031', '131', '1994-03-18', 'helena.lima@email.com', '81990000031', 3900.00, 32),
    ('10000000032', 'Igor Fernandes Costa', 'Rua da Paz', '50000032', '132', '1988-06-29', 'igor.costa@email.com', '81990000032', 5100.00, 38),
    ('10000000033', 'Jorge Luiz Santos', 'Rua Central', '50000033', '133', '1980-11-15', 'jorge.santos@email.com', '81990000033', 6700.00, 45),
    ('10000000034', 'Karen Alves Pereira', 'Rua Nova', '50000034', '134', '1997-02-09', 'karen.pereira@email.com', '81990000034', 3500.00, 29),
    ('10000000035', 'Larissa Gomes Silva', 'Rua Boa Vista', '50000035', '135', '1990-08-27', 'larissa.silva@email.com', '81990000035', 4600.00, 35),
    ('10000000036', 'Marcelo Barbosa Rocha', 'Rua Verde', '50000036', '136', '1985-04-03', 'marcelo.rocha@email.com', '81990000036', 5400.00, 41),
    ('10000000037', 'Natalia Carvalho Dias', 'Rua Principal', '50000037', '137', '1992-10-19', 'natalia.dias@email.com', '81990000037', 4100.00, 33),
    ('10000000038', 'Otavio Ribeiro Alves', 'Rua Esperanca', '50000038', '138', '1987-12-06', 'otavio.alves@email.com', '81990000038', 5200.00, 38),
    ('10000000039', 'Patricia Nunes Melo', 'Rua das Acacias', '50000039', '139', '1995-05-11', 'patricia.melo@email.com', '81990000039', 3700.00, 31),
    ('10000000040', 'Rafael Teixeira Souza', 'Rua do Parque', '50000040', '140', '1981-09-22', 'rafael.souza@email.com', '81990000040', 6100.00, 44),
    ('10000000041', 'Renata Campos Oliveira', 'Rua das Palmeiras', '50000041', '141', '1993-01-08', 'renata.oliveira@email.com', '81990000041', 4300.00, 33),
    ('10000000042', 'Rodrigo Freitas Lima', 'Rua do Lago', '50000042', '142', '1984-07-17', 'rodrigo.lima@email.com', '81990000042', 5800.00, 42),
    ('10000000043', 'Simone Batista Ramos', 'Rua do Norte', '50000043', '143', '1991-11-26', 'simone.ramos@email.com', '81990000043', 4000.00, 34),
    ('10000000044', 'Samuel Dias Moura', 'Rua da Amizade', '50000044', '144', '1989-03-13', 'samuel.moura@email.com', '81990000044', 5000.00, 37),
    ('10000000045', 'Tatiane Reis Barros', 'Rua da Estacao', '50000045', '145', '1996-06-24', 'tatiane.barros@email.com', '81990000045', 3600.00, 30),
    ('10000000046', 'Victor Moreira Lopes', 'Rua do Campo', '50000046', '146', '1982-02-18', 'victor.lopes@email.com', '81990000046', 6400.00, 44),
    ('10000000047', 'Viviane Cavalcante Maia', 'Rua do Mercado', '50000047', '147', '1994-09-29', 'viviane.maia@email.com', '81990000047', 4200.00, 31),
    ('10000000048', 'Wagner Martins Pinto', 'Rua do Bosque', '50000048', '148', '1986-05-07', 'wagner.pinto@email.com', '81990000048', 5500.00, 40),
    ('10000000049', 'Yasmin Fonseca Cardoso', 'Rua da Serra', '50000049', '149', '1998-12-16', 'yasmin.cardoso@email.com', '81990000049', 3300.00, 27),
    ('10000000050', 'Arthur Henrique Moraes', 'Rua do Porto', '50000050', '150', '1983-06-02', 'arthur.moraes@email.com', '81990000050', 6200.00, 43),
    ('10000000051', 'Alice Rodrigues Sales', 'Rua da Praia', '50000051', '151', '1990-10-25', 'alice.sales@email.com', '81990000051', 4400.00, 35),
    ('10000000052', 'Bernardo Martins Cunha', 'Rua do Centro', '50000052', '152', '1988-01-14', 'bernardo.cunha@email.com', '81990000052', 5300.00, 38),
    ('10000000053', 'Clara Monteiro Ramos', 'Rua do Jardim', '50000053', '153', '1995-03-21', 'clara.ramos@email.com', '81990000053', 3800.00, 31),
    ('10000000054', 'Davi Castro Vieira', 'Rua do Carmo', '50000054', '154', '1981-07-09', 'davi.vieira@email.com', '81990000054', 5900.00, 45),
    ('10000000055', 'Estela Correia Silva', 'Rua da Matriz', '50000055', '155', '1993-11-04', 'estela.silva@email.com', '81990000055', 4100.00, 32),
    ('10000000056', 'Fabio Martins Leite', 'Rua do Sol', '50000056', '156', '1985-08-16', 'fabio.leite@email.com', '81990000056', 5700.00, 40),
    ('10000000057', 'Isadora Souza Lima', 'Rua da Paz', '50000057', '157', '1997-04-28', 'isadora.lima@email.com', '81990000057', 3500.00, 29),
    ('10000000058', 'Leandro Fernandes Costa', 'Rua Central', '50000058', '158', '1984-12-11', 'leandro.costa@email.com', '81990000058', 5100.00, 41),
    ('10000000059', 'Manuela Alves Pereira', 'Rua Nova', '50000059', '159', '1992-06-30', 'manuela.pereira@email.com', '81990000059', 4000.00, 34),
    ('10000000060', 'Pedro Henrique Santos', 'Rua Boa Vista', '50000060', '160', '1987-09-05', 'pedro.santos@email.com', '81990000060', 5600.00, 38);

-- ============================================================
-- POVOAMENTO: DIRETOR
-- Quantidade: 15 tuplas
-- ============================================================

INSERT INTO diretor
    (cpf_diretor, data_inicio_mandato)
VALUES
    ('10000000001', '2010-01-01'),
    ('10000000002', '2011-02-02'),
    ('10000000003', '2012-03-03'),
    ('10000000004', '2013-04-04'),
    ('10000000005', '2014-05-05'),
    ('10000000006', '2015-06-06'),
    ('10000000007', '2016-07-07'),
    ('10000000008', '2017-08-08'),
    ('10000000009', '2018-09-09'),
    ('10000000010', '2019-10-10'),
    ('10000000011', '2020-11-11'),
    ('10000000012', '2021-12-12'),
    ('10000000013', '2022-01-13'),
    ('10000000014', '2023-02-14'),
    ('10000000015', '2010-03-15');

-- ============================================================
-- POVOAMENTO: JORNALISTA
-- Quantidade: 20 tuplas
-- ============================================================

INSERT INTO jornalista
    (cpf_jornalista, mtb)
VALUES
    ('10000000016', '10000-PE'),
    ('10000000017', '10001-PE'),
    ('10000000018', '10002-PE'),
    ('10000000019', '10003-PE'),
    ('10000000020', '10004-PE'),
    ('10000000021', '10005-PE'),
    ('10000000022', '10006-PE'),
    ('10000000023', '10007-PE'),
    ('10000000024', '10008-PE'),
    ('10000000025', '10009-PE'),
    ('10000000026', '10010-PE'),
    ('10000000027', '10011-PE'),
    ('10000000028', '10012-PE'),
    ('10000000029', '10013-PE'),
    ('10000000030', '10014-PE'),
    ('10000000031', '10015-PE'),
    ('10000000032', '10016-PE'),
    ('10000000033', '10017-PE'),
    ('10000000034', '10018-PE'),
    ('10000000035', '10019-PE');

-- ============================================================
-- POVOAMENTO: EDITOR_CHEFE
-- Quantidade: 15 tuplas
-- ============================================================

INSERT INTO editor_chefe
    (cpf_editor)
VALUES
    ('10000000036'),
    ('10000000037'),
    ('10000000038'),
    ('10000000039'),
    ('10000000040'),
    ('10000000041'),
    ('10000000042'),
    ('10000000043'),
    ('10000000044'),
    ('10000000045'),
    ('10000000046'),
    ('10000000047'),
    ('10000000048'),
    ('10000000049'),
    ('10000000050');

-- ============================================================
-- POVOAMENTO: EDITOR_ESPECIALIDADE
-- Quantidade: 22 tuplas (cada editor tem 1 especialidade; 7 tem 2)
-- ============================================================

INSERT INTO editor_especialidade
    (cpf_editor, especialidade)
VALUES
    ('10000000036', 'Política'),
    ('10000000036', 'Cultura'),
    ('10000000037', 'Economia'),
    ('10000000038', 'Esportes'),
    ('10000000038', 'Saúde'),
    ('10000000039', 'Cultura'),
    ('10000000040', 'Tecnologia'),
    ('10000000040', 'Meio Ambiente'),
    ('10000000041', 'Saúde'),
    ('10000000042', 'Educação'),
    ('10000000042', 'Investigativo'),
    ('10000000043', 'Meio Ambiente'),
    ('10000000044', 'Internacional'),
    ('10000000044', 'Economia'),
    ('10000000045', 'Investigativo'),
    ('10000000046', 'Política'),
    ('10000000046', 'Cultura'),
    ('10000000047', 'Economia'),
    ('10000000048', 'Esportes'),
    ('10000000048', 'Saúde'),
    ('10000000049', 'Cultura'),
    ('10000000050', 'Tecnologia'),
    ('10000000050', 'Meio Ambiente');

-- ============================================================
-- POVOAMENTO: JORNAL
-- Quantidade: 15 tuplas
-- ============================================================

INSERT INTO jornal
    (nome_jornal, cpf_diretor)
VALUES
    ('Jornal Pernambuco', '10000000001'),
    ('Diario do Recife', '10000000002'),
    ('Gazeta Pernambucana', '10000000003'),
    ('Folha Regional', '10000000004'),
    ('Noticias do Nordeste', '10000000005'),
    ('Jornal da Cidade', '10000000006'),
    ('Correio do Agreste', '10000000007'),
    ('Tribuna do Sertao', '10000000008'),
    ('Diario da Mata Sul', '10000000009'),
    ('Jornal do Litoral', '10000000010'),
    ('Gazeta do Vale', '10000000001'),
    ('Folha do Agreste', '10000000002'),
    ('Jornal Metropolitano', '10000000003'),
    ('Correio Regional', '10000000004'),
    ('Diario Popular', '10000000005');

-- ============================================================
-- POVOAMENTO: EDICAO
-- Quantidade: 60 tuplas (4 edicoes sequenciais por jornal)
-- ============================================================

INSERT INTO edicao
    (nome_jornal, numero_edicao, data)
VALUES
    ('Jornal Pernambuco', 1, '2026-02-06'),
    ('Jornal Pernambuco', 2, '2026-03-11'),
    ('Jornal Pernambuco', 3, '2026-04-16'),
    ('Jornal Pernambuco', 4, '2026-05-21'),

    ('Diario do Recife', 1, '2026-03-09'),
    ('Diario do Recife', 2, '2026-04-14'),
    ('Diario do Recife', 3, '2026-05-19'),
    ('Diario do Recife', 4, '2026-06-24'),

    ('Gazeta Pernambucana', 1, '2026-04-12'),
    ('Gazeta Pernambucana', 2, '2026-05-17'),
    ('Gazeta Pernambucana', 3, '2026-06-22'),
    ('Gazeta Pernambucana', 4, '2026-01-27'),

    ('Folha Regional', 1, '2026-05-15'),
    ('Folha Regional', 2, '2026-06-20'),
    ('Folha Regional', 3, '2026-01-25'),
    ('Folha Regional', 4, '2026-02-03'),

    ('Noticias do Nordeste', 1, '2026-06-18'),
    ('Noticias do Nordeste', 2, '2026-01-23'),
    ('Noticias do Nordeste', 3, '2026-02-01'),
    ('Noticias do Nordeste', 4, '2026-03-06'),

    ('Jornal da Cidade', 1, '2026-01-21'),
    ('Jornal da Cidade', 2, '2026-02-26'),
    ('Jornal da Cidade', 3, '2026-03-04'),
    ('Jornal da Cidade', 4, '2026-04-09'),

    ('Correio do Agreste', 1, '2026-02-24'),
    ('Correio do Agreste', 2, '2026-03-02'),
    ('Correio do Agreste', 3, '2026-04-07'),
    ('Correio do Agreste', 4, '2026-05-12'),

    ('Tribuna do Sertao', 1, '2026-03-27'),
    ('Tribuna do Sertao', 2, '2026-04-05'),
    ('Tribuna do Sertao', 3, '2026-05-10'),
    ('Tribuna do Sertao', 4, '2026-06-15'),

    ('Diario da Mata Sul', 1, '2026-04-03'),
    ('Diario da Mata Sul', 2, '2026-05-08'),
    ('Diario da Mata Sul', 3, '2026-06-13'),
    ('Diario da Mata Sul', 4, '2026-01-18'),

    ('Jornal do Litoral', 1, '2026-05-06'),
    ('Jornal do Litoral', 2, '2026-06-11'),
    ('Jornal do Litoral', 3, '2026-01-16'),
    ('Jornal do Litoral', 4, '2026-02-21'),

    ('Gazeta do Vale', 1, '2026-06-09'),
    ('Gazeta do Vale', 2, '2026-01-14'),
    ('Gazeta do Vale', 3, '2026-02-19'),
    ('Gazeta do Vale', 4, '2026-03-24'),

    ('Folha do Agreste', 1, '2026-01-12'),
    ('Folha do Agreste', 2, '2026-02-17'),
    ('Folha do Agreste', 3, '2026-03-22'),
    ('Folha do Agreste', 4, '2026-04-27'),

    ('Jornal Metropolitano', 1, '2026-02-15'),
    ('Jornal Metropolitano', 2, '2026-03-20'),
    ('Jornal Metropolitano', 3, '2026-04-25'),
    ('Jornal Metropolitano', 4, '2026-05-03'),

    ('Correio Regional', 1, '2026-03-18'),
    ('Correio Regional', 2, '2026-04-23'),
    ('Correio Regional', 3, '2026-05-01'),
    ('Correio Regional', 4, '2026-06-06'),

    ('Diario Popular', 1, '2026-04-21'),
    ('Diario Popular', 2, '2026-05-26'),
    ('Diario Popular', 3, '2026-06-04'),
    ('Diario Popular', 4, '2026-01-09');

-- ============================================================
-- POVOAMENTO: SETOR
-- Quantidade: 15 tuplas
-- ============================================================

INSERT INTO setor
    (id_setor, nome, descricao, cpf_editor_chefe)
VALUES
    (1, 'Política', 'Setor responsável pela cobertura política.', '10000000036'),
    (2, 'Economia', 'Setor responsável pelas notícias econômicas.', '10000000037'),
    (3, 'Esportes', 'Setor responsável pela cobertura esportiva.', '10000000038'),
    (4, 'Cultura', 'Setor responsável por notícias culturais.', '10000000039'),
    (5, 'Tecnologia', 'Setor responsável por tecnologia e inovação.', '10000000040'),
    (6, 'Saúde', 'Setor responsável por informações sobre saúde.', '10000000041'),
    (7, 'Educação', 'Setor responsável pela cobertura educacional.', '10000000042'),
    (8, 'Meio Ambiente', 'Setor responsável pelas questões ambientais.', '10000000043'),
    (9, 'Internacional', 'Setor responsável pelas notícias internacionais.', '10000000044'),
    (10, 'Brasil', 'Setor responsável pelas notícias nacionais.', '10000000045'),
    (11, 'Segurança', 'Setor responsável pela cobertura de segurança pública.', '10000000046'),
    (12, 'Entretenimento', 'Setor responsável por notícias de entretenimento.', '10000000047'),
    (13, 'Ciência', 'Setor responsável por ciência e pesquisa.', '10000000048'),
    (14, 'Cotidiano', 'Setor responsável pelas notícias do cotidiano.', '10000000049'),
    (15, 'Opinião', 'Setor responsável pelos conteúdos de opinião.', '10000000050');

-- ============================================================
-- POVOAMENTO: MATERIA
-- Quantidade: 60 tuplas
--
-- STATUS:
-- 0 = EM_ANDAMENTO
-- 1 = APROVADA
-- 2 = REPROVADA
-- ============================================================

INSERT INTO materia
    (titulo, subtitulo, resumo, conteudo, data, status, nome_jornal, numero_edicao, id_setor)
VALUES
    (
        'Nova política de desenvolvimento regional',
        'Medidas devem ampliar investimentos',
        'Governo apresenta novas medidas para o desenvolvimento regional.',
        'O programa prevê investimentos em infraestrutura, educação e tecnologia para estimular o desenvolvimento regional.',
        '2026-01-05',
        0,
        'Jornal Pernambuco',
        1,
        1
    ),
    (
        'Investimentos em educação avançam',
        'Novos projetos são anunciados',
        'Projetos educacionais devem beneficiar escolas públicas.',
        'As novas ações incluem reformas, aquisição de equipamentos e ampliação de programas educacionais.',
        '2026-01-06',
        1,
        'Jornal Pernambuco',
        2,
        2
    ),
    (
        'Tecnologia transforma serviços públicos',
        'Digitalização ganha espaço',
        'Órgãos públicos ampliam o uso de ferramentas digitais.',
        'A transformação digital busca reduzir burocracias e melhorar o atendimento oferecido à população.',
        '2026-01-07',
        2,
        'Jornal Pernambuco',
        3,
        3
    ),
    (
        'Novas ações para saúde pública',
        'Atendimento será ampliado',
        'Municípios anunciam medidas para melhorar os serviços de saúde.',
        'As iniciativas contemplam novas unidades, contratação de profissionais e modernização dos equipamentos.',
        '2026-01-08',
        0,
        'Jornal Pernambuco',
        4,
        4
    ),
    (
        'Mercado regional apresenta crescimento',
        'Comércio registra novos resultados',
        'Atividade comercial apresenta evolução no início do ano.',
        'Empresas locais registraram aumento nas vendas e esperam manter o crescimento nos próximos meses.',
        '2026-01-09',
        1,
        'Diario do Recife',
        1,
        5
    ),
    (
        'Programa ambiental é ampliado',
        'Municípios aderem à iniciativa',
        'Novas cidades passaram a integrar o programa de preservação ambiental.',
        'A iniciativa prevê ações de educação ambiental, recuperação de áreas degradadas e fiscalização.',
        '2026-01-10',
        2,
        'Diario do Recife',
        2,
        6
    ),
    (
        'Obras de infraestrutura são iniciadas',
        'Projeto prevê melhorias urbanas',
        'Novas obras devem melhorar a mobilidade urbana.',
        'O projeto inclui recuperação de vias, construção de equipamentos públicos e melhorias na iluminação.',
        '2026-01-11',
        0,
        'Diario do Recife',
        3,
        7
    ),
    (
        'Universidades ampliam projetos de pesquisa',
        'Ciência recebe novos investimentos',
        'Instituições anunciam novos projetos científicos.',
        'Os investimentos serão destinados a laboratórios, bolsas acadêmicas e desenvolvimento de pesquisas.',
        '2026-01-12',
        1,
        'Diario do Recife',
        4,
        8
    ),
    (
        'Empresas apostam em inovação',
        'Novas soluções chegam ao mercado',
        'Empresas regionais aumentam investimentos em inovação.',
        'Startups e empresas tradicionais estão desenvolvendo novas soluções para atender às demandas dos consumidores.',
        '2026-01-13',
        2,
        'Gazeta Pernambucana',
        1,
        9
    ),
    (
        'Transporte público passa por mudanças',
        'Novas rotas entram em planejamento',
        'Sistema de transporte deverá receber melhorias.',
        'O planejamento prevê novas linhas e mudanças nas rotas para atender regiões com maior demanda.',
        '2026-01-14',
        0,
        'Gazeta Pernambucana',
        2,
        10
    ),
    (
        'Agricultura familiar recebe incentivo',
        'Produtores terão novas oportunidades',
        'Programa busca fortalecer pequenos produtores.',
        'A iniciativa oferece assistência técnica, capacitação e acesso facilitado a programas de financiamento.',
        '2026-01-15',
        1,
        'Gazeta Pernambucana',
        3,
        11
    ),
    (
        'Comércio local se prepara para novas demandas',
        'Empresários investem em planejamento',
        'Comerciantes buscam estratégias para aumentar a competitividade.',
        'Empresários estão investindo em capacitação, tecnologia e melhoria da experiência dos consumidores.',
        '2026-01-16',
        2,
        'Gazeta Pernambucana',
        4,
        12
    ),
    (
        'Campanha de vacinação é iniciada',
        'Unidades recebem novas doses',
        'Campanha pretende ampliar a cobertura vacinal.',
        'As unidades de saúde estão preparadas para atender a população durante as novas etapas da campanha.',
        '2026-01-17',
        0,
        'Folha Regional',
        1,
        13
    ),
    (
        'Bibliotecas públicas recebem novos acervos',
        'Livros serão distribuídos',
        'Novos livros serão disponibilizados para leitores.',
        'A ação busca ampliar o acesso à leitura e fortalecer os espaços culturais dos municípios.',
        '2026-01-18',
        1,
        'Folha Regional',
        2,
        14
    ),
    (
        'Projeto de mobilidade é apresentado',
        'Estudo analisa alternativas',
        'Especialistas apresentam propostas para melhorar a mobilidade.',
        'O estudo avalia diferentes alternativas de transporte e infraestrutura para reduzir congestionamentos.',
        '2026-01-19',
        2,
        'Folha Regional',
        3,
        15
    ),
    (
        'Feira de tecnologia reúne empresas',
        'Evento apresenta novas soluções',
        'Empresas e pesquisadores participam de evento tecnológico.',
        'A programação inclui palestras, demonstrações de produtos e apresentação de projetos inovadores.',
        '2026-01-20',
        0,
        'Folha Regional',
        4,
        1
    ),
    (
        'Parques urbanos recebem melhorias',
        'Áreas de lazer serão revitalizadas',
        'Espaços públicos passam por obras de revitalização.',
        'As intervenções incluem novos equipamentos, iluminação e recuperação das áreas de convivência.',
        '2026-01-21',
        1,
        'Noticias do Nordeste',
        1,
        2
    ),
    (
        'Mercado de trabalho apresenta novas oportunidades',
        'Empresas anunciam vagas',
        'Novas oportunidades são disponibilizadas em diferentes setores.',
        'Empresas ampliaram seus processos seletivos para atender ao crescimento da demanda por profissionais.',
        '2026-01-22',
        2,
        'Noticias do Nordeste',
        2,
        3
    ),
    (
        'Centro cultural recebe programação especial',
        'Eventos serão realizados durante o mês',
        'Centro cultural anuncia novas atividades.',
        'A programação reúne exposições, oficinas, apresentações musicais e atividades educativas.',
        '2026-01-23',
        0,
        'Noticias do Nordeste',
        3,
        4
    ),
    (
        'Novas medidas para segurança urbana',
        'Projeto prevê ações integradas',
        'Órgãos públicos estudam novas medidas de segurança.',
        'O projeto prevê integração entre diferentes instituições e utilização de novas ferramentas tecnológicas.',
        '2026-01-24',
        1,
        'Noticias do Nordeste',
        4,
        5
    ),
    (
        'Pesquisa aponta mudanças no consumo',
        'Hábitos dos consumidores são analisados',
        'Estudo identifica novas tendências de consumo.',
        'A pesquisa aponta mudanças no comportamento dos consumidores e crescimento das compras digitais.',
        '2026-01-25',
        2,
        'Jornal da Cidade',
        1,
        6
    ),
    (
        'Município amplia coleta seletiva',
        'Novos bairros serão atendidos',
        'Programa de coleta seletiva será expandido.',
        'A expansão pretende aumentar o volume de materiais reciclados e conscientizar os moradores.',
        '2026-01-26',
        0,
        'Jornal da Cidade',
        2,
        7
    ),
    (
        'Escolas recebem equipamentos tecnológicos',
        'Salas terão novos recursos',
        'Instituições de ensino recebem novos equipamentos.',
        'Computadores, projetores e outros recursos tecnológicos serão utilizados nas atividades pedagógicas.',
        '2026-01-27',
        1,
        'Jornal da Cidade',
        3,
        8
    ),
    (
        'Evento esportivo movimenta a cidade',
        'Competição reúne atletas',
        'Evento esportivo reúne participantes de diferentes municípios.',
        'A competição contará com diversas modalidades e atividades abertas ao público.',
        '2026-01-28',
        2,
        'Jornal da Cidade',
        4,
        9
    ),
    (
        'Plano de turismo é atualizado',
        'Setor busca novos visitantes',
        'Novas estratégias são apresentadas para o turismo regional.',
        'O plano pretende divulgar os principais destinos e melhorar a infraestrutura turística.',
        '2026-01-29',
        0,
        'Correio do Agreste',
        1,
        10
    ),
    (
        'Novas oportunidades para pequenos negócios',
        'Programa oferece capacitação',
        'Empreendedores terão acesso a novos cursos.',
        'O programa oferece capacitação em gestão, marketing, finanças e planejamento empresarial.',
        '2026-01-30',
        1,
        'Correio do Agreste',
        2,
        11
    ),
    (
        'Hospital recebe novos equipamentos',
        'Atendimento especializado será ampliado',
        'Unidade de saúde passa por modernização.',
        'Os novos equipamentos permitirão ampliar a capacidade de atendimento e realizar novos procedimentos.',
        '2026-02-01',
        2,
        'Correio do Agreste',
        3,
        12
    ),
    (
        'Programa cultural chega a novas comunidades',
        'Atividades serão realizadas gratuitamente',
        'Projeto cultural amplia suas ações.',
        'Oficinas e apresentações serão realizadas em diferentes comunidades durante os próximos meses.',
        '2026-02-02',
        0,
        'Correio do Agreste',
        4,
        13
    ),
    (
        'Novas medidas apoiam estudantes',
        'Programa oferece auxílio',
        'Estudantes poderão receber apoio para continuar os estudos.',
        'O programa prevê auxílio financeiro e acompanhamento educacional para estudantes em situação de vulnerabilidade.',
        '2026-02-03',
        1,
        'Tribuna do Sertao',
        1,
        14
    ),
    (
        'Empresas investem em energia renovável',
        'Projetos sustentáveis ganham espaço',
        'Empresas anunciam novos projetos de energia limpa.',
        'Os projetos incluem instalação de sistemas solares e medidas para reduzir o consumo energético.',
        '2026-02-04',
        2,
        'Tribuna do Sertao',
        2,
        15
    ),
    (
        'Obras de saneamento avançam',
        'Novas áreas serão atendidas',
        'Projeto de saneamento entra em nova etapa.',
        'As obras incluem expansão da rede de abastecimento e implantação de sistemas de tratamento.',
        '2026-02-05',
        0,
        'Tribuna do Sertao',
        3,
        1
    ),
    (
        'Centro de inovação inicia atividades',
        'Espaço reúne empreendedores',
        'Novo centro pretende estimular projetos inovadores.',
        'O espaço oferecerá infraestrutura, capacitação e oportunidades de colaboração entre empresas.',
        '2026-02-06',
        1,
        'Tribuna do Sertao',
        4,
        2
    ),
    (
        'Campanha de prevenção é lançada',
        'Ações serão realizadas durante o mês',
        'Campanha busca conscientizar a população.',
        'As atividades incluem palestras, distribuição de materiais informativos e atendimento especializado.',
        '2026-02-07',
        2,
        'Diario da Mata Sul',
        1,
        3
    ),
    (
        'Novo sistema facilita atendimento',
        'Serviço passa a funcionar digitalmente',
        'Plataforma digital começa a ser utilizada.',
        'O novo sistema permite que usuários acompanhem solicitações e realizem procedimentos pela internet.',
        '2026-02-08',
        0,
        'Diario da Mata Sul',
        2,
        4
    ),
    (
        'Festival regional anuncia programação',
        'Evento terá atrações diversas',
        'Festival prepara programação para o público.',
        'O evento contará com apresentações artísticas, atividades culturais e espaços destinados à gastronomia.',
        '2026-02-09',
        1,
        'Diario da Mata Sul',
        3,
        5
    ),
    (
        'Novas linhas de crédito são disponibilizadas',
        'Empreendedores poderão solicitar financiamento',
        'Instituições anunciam novas condições de crédito.',
        'As linhas de financiamento possuem condições específicas para pequenos e médios empreendedores.',
        '2026-02-10',
        2,
        'Diario da Mata Sul',
        4,
        6
    ),
    (
        'Projeto de arborização é ampliado',
        'Mais áreas receberão árvores',
        'Município amplia ações de arborização urbana.',
        'O projeto prevê o plantio de árvores em ruas, praças e áreas públicas.',
        '2026-02-11',
        0,
        'Jornal do Litoral',
        1,
        7
    ),
    (
        'Cursos profissionalizantes são anunciados',
        'Novas turmas serão abertas',
        'Programa oferece capacitação profissional.',
        'Os cursos abrangem diferentes áreas e pretendem facilitar a entrada dos participantes no mercado de trabalho.',
        '2026-02-12',
        1,
        'Jornal do Litoral',
        2,
        8
    ),
    (
        'Museu prepara nova exposição',
        'Acervo histórico será apresentado',
        'Museu anuncia exposição sobre a história regional.',
        'A exposição reúne documentos, fotografias e objetos que fazem parte da história da região.',
        '2026-02-13',
        2,
        'Jornal do Litoral',
        3,
        9
    ),
    (
        'Plano habitacional recebe novas propostas',
        'Projeto busca ampliar moradias',
        'Novas propostas são analisadas pelo poder público.',
        'O plano prevê construção de unidades habitacionais e melhorias em áreas já ocupadas.',
        '2026-02-14',
        0,
        'Jornal do Litoral',
        4,
        10
    ),
    (
        'Empresas adotam novas práticas ambientais',
        'Sustentabilidade ganha destaque',
        'Empresas ampliam suas ações ambientais.',
        'As iniciativas incluem redução de resíduos, economia de água e utilização de fontes renováveis.',
        '2026-02-15',
        1,
        'Gazeta do Vale',
        1,
        11
    ),
    (
        'Bibliotecas ampliam horários de atendimento',
        'Serviço será disponibilizado aos finais de semana',
        'Bibliotecas passam a atender em novos horários.',
        'A mudança pretende facilitar o acesso da população aos espaços de leitura e pesquisa.',
        '2026-02-16',
        2,
        'Gazeta do Vale',
        2,
        12
    ),
    (
        'Projeto esportivo atende novos jovens',
        'Atividades gratuitas são oferecidas',
        'Projeto amplia o atendimento a crianças e adolescentes.',
        'As atividades esportivas serão realizadas em diferentes espaços públicos.',
        '2026-02-17',
        0,
        'Gazeta do Vale',
        3,
        13
    ),
    (
        'Novas tecnologias chegam à agricultura',
        'Produtores adotam ferramentas digitais',
        'Tecnologia começa a ser utilizada no campo.',
        'Sensores, sistemas de monitoramento e ferramentas digitais ajudam produtores a melhorar a produtividade.',
        '2026-02-18',
        1,
        'Gazeta do Vale',
        4,
        14
    ),
    (
        'Plano de emergência é atualizado',
        'Órgãos revisam procedimentos',
        'Plano municipal passa por atualização.',
        'As mudanças buscam melhorar a capacidade de resposta das equipes em situações de emergência.',
        '2026-02-19',
        2,
        'Folha do Agreste',
        1,
        15
    ),
    (
        'Novas ações para geração de empregos',
        'Programa aproxima empresas e trabalhadores',
        'Projeto busca facilitar a contratação de profissionais.',
        'A iniciativa pretende aproximar empresas que possuem vagas disponíveis de trabalhadores em busca de oportunidades.',
        '2026-02-20',
        0,
        'Folha do Agreste',
        2,
        1
    ),
    (
        'Feira de negócios reúne empreendedores',
        'Evento promove parcerias',
        'Empresários participam de feira regional.',
        'O encontro promove oportunidades de negócios, palestras e apresentação de novos produtos.',
        '2026-02-21',
        1,
        'Folha do Agreste',
        3,
        2
    ),
    (
        'Programa de leitura incentiva estudantes',
        'Escolas recebem novas atividades',
        'Projeto incentiva o hábito da leitura.',
        'As atividades incluem rodas de leitura, oficinas de escrita e encontros com autores.',
        '2026-02-22',
        2,
        'Folha do Agreste',
        4,
        3
    ),
    (
        'Novas medidas de proteção ambiental',
        'Fiscalização será reforçada',
        'Órgãos ambientais anunciam novas ações.',
        'As medidas incluem fiscalização de áreas protegidas e ações educativas junto às comunidades.',
        '2026-02-23',
        0,
        'Jornal Metropolitano',
        1,
        4
    ),
    (
        'Centro esportivo passa por reforma',
        'Espaço terá novos equipamentos',
        'Centro esportivo será modernizado.',
        'A reforma prevê melhorias nas quadras, vestiários e espaços destinados aos usuários.',
        '2026-02-24',
        1,
        'Jornal Metropolitano',
        2,
        5
    ),
    (
        'Pesquisa analisa desenvolvimento econômico',
        'Estudo reúne dados regionais',
        'Pesquisadores analisam indicadores econômicos.',
        'O levantamento considera dados de emprego, renda, produção e atividade empresarial.',
        '2026-02-25',
        2,
        'Jornal Metropolitano',
        3,
        6
    ),
    (
        'Novos serviços digitais são disponibilizados',
        'Usuários poderão realizar solicitações online',
        'Plataforma pública recebe novas funcionalidades.',
        'Os novos serviços permitem realizar solicitações sem necessidade de atendimento presencial.',
        '2026-02-26',
        0,
        'Jornal Metropolitano',
        4,
        7
    ),
    (
        'Projeto de capacitação tecnológica',
        'Cursos serão oferecidos gratuitamente',
        'Programa pretende ampliar conhecimentos digitais.',
        'Os participantes poderão aprender conceitos de informática, programação e ferramentas digitais.',
        '2026-02-27',
        1,
        'Correio Regional',
        1,
        8
    ),
    (
        'Novos investimentos em infraestrutura',
        'Recursos serão destinados a obras',
        'Governo anuncia novos investimentos.',
        'Os recursos serão destinados à melhoria de estradas, prédios públicos e sistemas urbanos.',
        '2026-02-28',
        2,
        'Correio Regional',
        2,
        9
    ),
    (
        'Campanha incentiva consumo consciente',
        'Ações educativas serão realizadas',
        'Projeto busca incentivar hábitos sustentáveis.',
        'A campanha apresenta orientações para redução do desperdício e consumo responsável.',
        '2026-03-01',
        0,
        'Correio Regional',
        3,
        10
    ),
    (
        'Novas oportunidades no setor de serviços',
        'Empresas ampliam contratações',
        'Setor de serviços apresenta novas oportunidades.',
        'Empresas estão ampliando suas equipes diante do aumento da demanda por serviços especializados.',
        '2026-03-02',
        1,
        'Correio Regional',
        4,
        11
    ),
    (
        'Programa de inovação recebe inscrições',
        'Empreendedores podem participar',
        'Programa abre inscrições para novos projetos.',
        'Os participantes poderão apresentar projetos inovadores e receber orientação técnica.',
        '2026-03-03',
        2,
        'Diario Popular',
        1,
        12
    ),
    (
        'Projeto cultural recebe novos recursos',
        'Atividades serão ampliadas',
        'Projeto cultural recebe investimento adicional.',
        'Os novos recursos permitirão ampliar oficinas, apresentações e atividades educativas.',
        '2026-03-04',
        0,
        'Diario Popular',
        2,
        13
    ),
    (
        'Sistema de transporte recebe melhorias',
        'Novos equipamentos serão instalados',
        'Sistema passa por modernização.',
        'Novos equipamentos deverão melhorar o controle e o funcionamento do transporte público.',
        '2026-03-05',
        1,
        'Diario Popular',
        3,
        14
    ),
    (
        'Ações de saúde preventiva são ampliadas',
        'Equipes atenderão novas regiões',
        'Programa de prevenção amplia seu alcance.',
        'As equipes realizarão atendimentos e atividades educativas em diferentes regiões.',
        '2026-03-06',
        2,
        'Diario Popular',
        4,
        15
    );

-- ============================================================
-- POVOAMENTO: ALOCACAO_JORNALISTA_MATERIA
-- Quantidade: 60 tuplas
-- ============================================================

INSERT INTO alocacao_jornalista_materia
    (cpf_jornalista, id_materia)
VALUES
    ('10000000016', 1),
    ('10000000017', 2),
    ('10000000018', 3),
    ('10000000019', 4),
    ('10000000020', 5),
    ('10000000021', 6),
    ('10000000022', 7),
    ('10000000023', 8),
    ('10000000024', 9),
    ('10000000025', 10),
    ('10000000026', 11),
    ('10000000027', 12),
    ('10000000028', 13),
    ('10000000029', 14),
    ('10000000030', 15),
    ('10000000031', 16),
    ('10000000032', 17),
    ('10000000033', 18),
    ('10000000034', 19),
    ('10000000035', 20),
    ('10000000016', 21),
    ('10000000017', 22),
    ('10000000018', 23),
    ('10000000019', 24),
    ('10000000020', 25),
    ('10000000021', 26),
    ('10000000022', 27),
    ('10000000023', 28),
    ('10000000024', 29),
    ('10000000025', 30),
    ('10000000026', 31),
    ('10000000027', 32),
    ('10000000028', 33),
    ('10000000029', 34),
    ('10000000030', 35),
    ('10000000031', 36),
    ('10000000032', 37),
    ('10000000033', 38),
    ('10000000034', 39),
    ('10000000035', 40),
    ('10000000016', 41),
    ('10000000017', 42),
    ('10000000018', 43),
    ('10000000019', 44),
    ('10000000020', 45),
    ('10000000021', 46),
    ('10000000022', 47),
    ('10000000023', 48),
    ('10000000024', 49),
    ('10000000025', 50),
    ('10000000026', 51),
    ('10000000027', 52),
    ('10000000028', 53),
    ('10000000029', 54),
    ('10000000030', 55),
    ('10000000031', 56),
    ('10000000032', 57),
    ('10000000033', 58),
    ('10000000034', 59),
    ('10000000035', 60);
