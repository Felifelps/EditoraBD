from typing import Any

from psycopg import Connection
from psycopg.rows import dict_row


class MateriaRepository:

    def __init__(self, conn: Connection):
        self.conn = conn

    def listar_todas(
        self,
        search: str | None = None,
        status: int | None = None,
        setor_id: int | None = None,
    ) -> list[dict[str, Any]]:
        query = """
            SELECT
                m.id_materia,
                m.titulo,
                m.subtitulo,
                m.resumo,
                m.conteudo,
                m.data,
                m.status,
                m.nome_jornal,
                m.numero_edicao,
                m.id_setor
            FROM materia m
            WHERE 1 = 1
        """

        params: list[Any] = []

        if search:
            query += """
                AND m.titulo ILIKE %s
            """
            params.append(f"%{search}%")

        if status is not None:
            query += """
                AND m.status = %s
            """
            params.append(status)

        if setor_id is not None:
            query += """
                AND m.id_setor = %s
            """
            params.append(setor_id)

        query += """
            ORDER BY m.id_materia ASC
        """

        with self.conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()

    def buscar_por_id(
        self,
        id_materia: int,
    ) -> dict[str, Any] | None:
        query = """
            SELECT
                m.id_materia,
                m.titulo,
                m.subtitulo,
                m.resumo,
                m.conteudo,
                m.data,
                m.status,
                m.nome_jornal,
                m.numero_edicao,
                m.id_setor
            FROM materia m
            WHERE m.id_materia = %s
        """

        with self.conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(query, (id_materia,))
            return cursor.fetchone()

    def buscar_duplicada(
        self,
        titulo: str,
        data,
        nome_jornal: str | None,
        numero_edicao: int | None,
        id_setor: int | None,
        id_materia: int | None = None,
    ) -> dict[str, Any] | None:
        query = """
            SELECT
                m.id_materia,
                m.titulo,
                m.data,
                m.nome_jornal,
                m.numero_edicao,
                m.id_setor
            FROM materia m
            WHERE m.titulo = %s
              AND m.data = %s
              AND m.nome_jornal IS NOT DISTINCT FROM %s
              AND m.numero_edicao IS NOT DISTINCT FROM %s
              AND m.id_setor IS NOT DISTINCT FROM %s
        """

        params: list[Any] = [
            titulo,
            data,
            nome_jornal,
            numero_edicao,
            id_setor,
        ]

        if id_materia is not None:
            query += """
                AND m.id_materia <> %s
            """
            params.append(id_materia)

        with self.conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(query, params)
            return cursor.fetchone()

    def criar(
        self,
        dados: dict[str, Any],
    ) -> dict[str, Any]:
        query = """
            INSERT INTO materia (
                titulo,
                subtitulo,
                resumo,
                conteudo,
                data,
                status,
                nome_jornal,
                numero_edicao,
                id_setor
            )
            VALUES (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s
            )
            RETURNING
                id_materia,
                titulo,
                subtitulo,
                resumo,
                conteudo,
                data,
                status,
                nome_jornal,
                numero_edicao,
                id_setor
        """

        values = (
            dados["titulo"],
            dados["subtitulo"],
            dados["resumo"],
            dados["conteudo"],
            dados["data"],
            dados["status"],
            dados["nome_jornal"],
            dados["numero_edicao"],
            dados["id_setor"],
        )

        with self.conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(query, values)
            materia = cursor.fetchone()

        self.conn.commit()

        return materia

    def atualizar(
        self,
        id_materia: int,
        dados: dict[str, Any],
    ) -> dict[str, Any] | None:
        query = """
            UPDATE materia
            SET
                titulo = %s,
                subtitulo = %s,
                resumo = %s,
                conteudo = %s,
                data = %s,
                status = %s,
                nome_jornal = %s,
                numero_edicao = %s,
                id_setor = %s
            WHERE id_materia = %s
            RETURNING
                id_materia,
                titulo,
                subtitulo,
                resumo,
                conteudo,
                data,
                status,
                nome_jornal,
                numero_edicao,
                id_setor
        """

        values = (
            dados["titulo"],
            dados["subtitulo"],
            dados["resumo"],
            dados["conteudo"],
            dados["data"],
            dados["status"],
            dados["nome_jornal"],
            dados["numero_edicao"],
            dados["id_setor"],
            id_materia,
        )

        with self.conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(query, values)
            materia = cursor.fetchone()

        self.conn.commit()

        return materia

    def atualizar_status(
        self,
        id_materia: int,
        novo_status: int,
    ) -> bool:
        query = """
            UPDATE materia
            SET status = %s
            WHERE id_materia = %s
        """

        with self.conn.cursor() as cursor:
            cursor.execute(
                query,
                (
                    novo_status,
                    id_materia,
                ),
            )

            atualizado = cursor.rowcount > 0

        self.conn.commit()

        return atualizado

    def deletar(
        self,
        id_materia: int,
    ) -> bool:
        query = """
            DELETE FROM materia
            WHERE id_materia = %s
        """

        with self.conn.cursor() as cursor:
            cursor.execute(query, (id_materia,))
            removido = cursor.rowcount > 0

        self.conn.commit()

        return removido

    def listar_jornalistas(
        self,
        materia_id: int,
    ) -> list[dict[str, Any]]:
        query = """
            SELECT
                a.cpf_jornalista
            FROM alocacao_jornalista_materia a
            WHERE a.id_materia = %s
            ORDER BY a.cpf_jornalista
        """

        with self.conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(query, (materia_id,))
            return cursor.fetchall()

    def vincular_jornalista(
        self,
        materia_id: int,
        jornalista_cpf: str,
    ) -> None:
        query = """
            INSERT INTO alocacao_jornalista_materia (
                id_materia,
                cpf_jornalista
            )
            VALUES (%s, %s)
            ON CONFLICT DO NOTHING
        """

        with self.conn.cursor() as cursor:
            cursor.execute(
                query,
                (
                    materia_id,
                    jornalista_cpf,
                ),
            )

        self.conn.commit()

    def desvincular_jornalista(
        self,
        materia_id: int,
        jornalista_cpf: str,
    ) -> None:
        query = """
            DELETE FROM alocacao_jornalista_materia
            WHERE id_materia = %s
              AND cpf_jornalista = %s
        """

        with self.conn.cursor() as cursor:
            cursor.execute(
                query,
                (
                    materia_id,
                    jornalista_cpf,
                ),
            )

        self.conn.commit()