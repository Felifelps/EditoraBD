CREATE OR REPLACE VIEW vw_historico_status_materia AS
SELECT
    h.id,
    h.id_materia,
    m.titulo,
    CASE h.status_anterior
        WHEN 0 THEN 'Reprovada'
        WHEN 1 THEN 'Aprovada'
        WHEN 2 THEN 'Em Andamento'
    END AS status_anterior_texto,
    CASE h.status_novo
        WHEN 0 THEN 'Reprovada'
        WHEN 1 THEN 'Aprovada'
        WHEN 2 THEN 'Em Andamento'
    END AS status_novo_texto,
    h.alterado_em
FROM historico_status_materia h
JOIN materia m ON h.id_materia = m.id_materia;
