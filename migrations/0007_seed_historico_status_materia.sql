-- ============================================================
-- SEED — trilha de auditoria de status de materia
-- Exercita a trigger trg_historico_status_materia (migration 0005) para que o
-- relatorio "Historico de status de materia" ja tenha dados logo apos o
-- `docker compose up`, sem depender de o usuario aprovar/reprovar algo antes.
--
-- Cada materia percorre os outros dois status e VOLTA ao status original, entao
-- o estado final do seed nao muda — so passa a existir historico registrado
-- automaticamente pela trigger (status_anterior, status_novo, alterado_em).
-- ============================================================

DO $$
DECLARE
    materia_row RECORD;
BEGIN
    FOR materia_row IN
        SELECT id_materia, status AS status_original
        FROM materia
        ORDER BY id_materia
        LIMIT 12
    LOOP
        UPDATE materia
            SET status = (materia_row.status_original + 1) % 3
            WHERE id_materia = materia_row.id_materia;

        UPDATE materia
            SET status = (materia_row.status_original + 2) % 3
            WHERE id_materia = materia_row.id_materia;

        UPDATE materia
            SET status = materia_row.status_original
            WHERE id_materia = materia_row.id_materia;
    END LOOP;
END $$;
