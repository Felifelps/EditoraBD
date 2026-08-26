-- ============================================================
-- TRIGGER — historico de mudancas de status de materia
-- Requisito da entrega: no minimo 1 trigger funcional no banco, com foco
-- em auditoria/integridade. Registra toda mudanca de materia.status numa
-- tabela de auditoria, sem depender de nenhuma logica no backend — funciona
-- mesmo que o status seja alterado por um UPDATE direto no banco.
-- ============================================================

CREATE TABLE IF NOT EXISTS historico_status_materia (
    id              SERIAL PRIMARY KEY,
    id_materia      INT NOT NULL,
    status_anterior INT NOT NULL,
    status_novo     INT NOT NULL,
    alterado_em     TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT fk_historico_status_materia_materia
        FOREIGN KEY (id_materia)
        REFERENCES materia(id_materia)
        ON DELETE CASCADE
);

CREATE OR REPLACE FUNCTION fn_registrar_historico_status_materia()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.status IS DISTINCT FROM NEW.status THEN
        INSERT INTO historico_status_materia (
            id_materia,
            status_anterior,
            status_novo
        )
        VALUES (
            NEW.id_materia,
            OLD.status,
            NEW.status
        );
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_historico_status_materia ON materia;

CREATE TRIGGER trg_historico_status_materia
    AFTER UPDATE OF status ON materia
    FOR EACH ROW
    EXECUTE FUNCTION fn_registrar_historico_status_materia();
