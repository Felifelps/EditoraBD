-- View 1: Resumo de edicoes por jornal (une jornal, diretor, funcionario e edicao)
-- Motivo: Ajuda a entender rapidamente a volumetria de edições publicadas por cada jornal e quem e o diretor responsavel, util para relatorios gerenciais de producao.
CREATE OR REPLACE VIEW vw_resumo_edicoes_jornal AS
SELECT
    j.nome_jornal,
    f.nome AS nome_diretor,
    COUNT(e.numero_edicao) AS total_edicoes,
    MAX(e.data) AS ultima_edicao
FROM jornal j
JOIN diretor d ON j.cpf_diretor = d.cpf_diretor
JOIN funcionario f ON d.cpf_diretor = f.cpf
LEFT JOIN edicao e ON j.nome_jornal = e.nome_jornal
GROUP BY j.nome_jornal, f.nome;

-- View 2: Carga de materias por jornalista (une jornalista, funcionario, alocacao_jornalista_materia e materia)
-- Motivo: Fornece um relatorio de produtividade para Editores e Diretores avaliarem o volume de trabalho e a taxa de aprovacao das materias de cada jornalista.
CREATE OR REPLACE VIEW vw_carga_materias_jornalista AS
SELECT
    j.cpf_jornalista,
    f.nome AS nome_jornalista,
    j.mtb,
    COUNT(m.id_materia) AS total_materias,
    SUM(CASE WHEN m.status = 1 THEN 1 ELSE 0 END) AS materias_aprovadas,
    SUM(CASE WHEN m.status = 0 THEN 1 ELSE 0 END) AS materias_reprovadas,
    SUM(CASE WHEN m.status = 2 THEN 1 ELSE 0 END) AS materias_em_andamento
FROM jornalista j
JOIN funcionario f ON j.cpf_jornalista = f.cpf
LEFT JOIN alocacao_jornalista_materia ajm ON j.cpf_jornalista = ajm.cpf_jornalista
LEFT JOIN materia m ON ajm.id_materia = m.id_materia
GROUP BY j.cpf_jornalista, f.nome, j.mtb;

-- View 3: Setores com editor-chefe e especialidades (une setor, editor_chefe, funcionario e editor_especialidade)
-- Motivo: Simplifica a interface de listagem de setores, exibindo imediatamente qual e o editor-chefe responsavel e o seu perfil (especialidades), o que de outra forma exigiria consultas complexas.
CREATE OR REPLACE VIEW vw_setores_editores AS
SELECT
    s.id_setor,
    s.nome AS nome_setor,
    s.descricao AS descricao_setor,
    ec.cpf_editor AS cpf_editor_chefe,
    f.nome AS nome_editor,
    STRING_AGG(ee.especialidade, ', ') AS especialidades
FROM setor s
JOIN editor_chefe ec ON s.cpf_editor_chefe = ec.cpf_editor
JOIN funcionario f ON ec.cpf_editor = f.cpf
LEFT JOIN editor_especialidade ee ON ec.cpf_editor = ee.cpf_editor
GROUP BY s.id_setor, s.nome, s.descricao, ec.cpf_editor, f.nome;

-- View 4: Detalhes gerais de funcionarios (une funcionario, diretor, jornalista e editor_chefe)
-- Motivo: Resolve a complexidade de consultas da heranca de classes no banco de dados. Permite listar todos os funcionários, identificando dinamicamente seus cargos e trazendo campos especificos em uma unica requisicao.
CREATE OR REPLACE VIEW vw_funcionarios_detalhes AS
SELECT
    f.cpf,
    f.nome,
    f.email,
    f.telefone,
    f.salario,
    d.data_inicio_mandato,
    j.mtb,
    CASE
        WHEN ec.cpf_editor IS NOT NULL THEN 'Editor-Chefe'
        WHEN j.cpf_jornalista IS NOT NULL THEN 'Jornalista'
        WHEN d.cpf_diretor IS NOT NULL THEN 'Diretor'
        ELSE 'Funcionario'
    END AS cargo
FROM funcionario f
LEFT JOIN diretor d ON f.cpf = d.cpf_diretor
LEFT JOIN jornalista j ON f.cpf = j.cpf_jornalista
LEFT JOIN editor_chefe ec ON f.cpf = ec.cpf_editor;

-- View 5: Catalogo completo de materias (une materia, setor, edicao, alocacao_jornalista_materia e funcionario)
-- Motivo: Extremamente util para alimentar paginas de feed ou tabelas ricas no front-end, agrupando os multiplos autores (jornalistas) de uma mesma materia e traduzindo o status numerico para texto legivel.
CREATE OR REPLACE VIEW vw_materias_completas AS
SELECT
    m.id_materia,
    m.titulo,
    m.data AS data_materia,
    CASE m.status
        WHEN 0 THEN 'Reprovada'
        WHEN 1 THEN 'Aprovada'
        WHEN 2 THEN 'Em Andamento'
    END AS status_texto,
    s.nome AS nome_setor,
    e.numero_edicao,
    e.nome_jornal,
    STRING_AGG(f.nome, ', ') AS autores
FROM materia m
JOIN setor s ON m.id_setor = s.id_setor
JOIN edicao e ON m.nome_jornal = e.nome_jornal AND m.numero_edicao = e.numero_edicao
LEFT JOIN alocacao_jornalista_materia ajm ON m.id_materia = ajm.id_materia
LEFT JOIN jornalista j ON ajm.cpf_jornalista = j.cpf_jornalista
LEFT JOIN funcionario f ON j.cpf_jornalista = f.cpf
GROUP BY m.id_materia, s.nome, e.numero_edicao, e.nome_jornal, m.status, m.titulo, m.data;
