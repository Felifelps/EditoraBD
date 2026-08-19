# Queries de materia (criar, submeter, aprovar, reprovar, alocar jornalista).

from typing import Any, Dict, List, Optional
from psycopg import Connection
from psycopg.rows import dict_row

from app.schemas.materias import MateriaCriar, MateriaAtualizar


class MateriaRepository:

    def __init__(self, conn: Connection):
        self.conn = conn

    def listar_todas(
        self,
        search: Optional[str] = None,
        status: Optional[int] = None,
        setor_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Lista todas as matérias aplicando filtros opcionais."""
        query = """
            SELECT id_materia, titulo, subtitulo, resumo, conteudo, data,
                   status, nome_jornal, numero_edicao, id_setor, cpf_editor_chefe
            FROM materia
            WHERE (%s::TEXT IS NULL OR titulo ILIKE '%%' || %s || '%%')
              AND (%s::INT IS NULL OR status = %s)
              AND (%s::INT IS NULL OR id_setor = %s);
        """
        with self.conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                query,
                (search, search, status, status, setor_id, setor_id)
            )
            return cursor.fetchall()

    def buscar_por_id(self, id_materia: int) -> Optional[Dict[str, Any]]:
        """Busca uma matéria específica pelo seu ID."""
        query = """
            SELECT id_materia, titulo, subtitulo, resumo, conteudo, data,
                   status, nome_jornal, numero_edicao, id_setor, cpf_editor_chefe
            FROM materia
            WHERE id_materia = %s;
        """
        with self.conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(query, (id_materia,))
            return cursor.fetchone()

    def criar(self, dados: MateriaCriar) -> Dict[str, Any]:
        """Insere uma nova matéria no banco de dados."""
        query = """
            INSERT INTO materia (
                titulo, subtitulo, resumo, conteudo, data,
                status, nome_jornal, numero_edicao, id_setor, cpf_editor_chefe
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id_materia, titulo, subtitulo, resumo, conteudo, data,
                      status, nome_jornal, numero_edicao, id_setor, cpf_editor_chefe;
        """
        with self.conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                query,
                (
                    dados.titulo,
                    dados.subtitulo,
                    dados.resumo,
                    dados.conteudo,
                    dados.data,
                    dados.status,
                    dados.nome_jornal,
                    dados.numero_edicao,
                    dados.id_setor,
                    dados.cpf_editor_chefe,
                ),
            )
            self.conn.commit()
            return cursor.fetchone()

    def atualizar(
        self,
        id_materia: int,
        dados: MateriaAtualizar
    ) -> Optional[Dict[str, Any]]:
        """Atualiza os dados de uma matéria existente de forma dinâmica."""
        dados_dict = dados.model_dump(exclude_unset=True)

        if not dados_dict:
            return self.buscar_por_id(id_materia)

        campos = []
        valores = []

        for coluna, valor in dados_dict.items():
            campos.append(f"{coluna} = %s")
            valores.append(valor)

        valores.append(id_materia)

        query = f"""
            UPDATE materia
            SET {", ".join(campos)}
            WHERE id_materia = %s
            RETURNING id_materia, titulo, subtitulo, resumo, conteudo, data,
                      status, nome_jornal, numero_edicao, id_setor, cpf_editor_chefe;
        """

        with self.conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(query, tuple(valores))
            self.conn.commit()
            return cursor.fetchone()

    def atualizar_status(self, id_materia: int, novo_status: int) -> bool:
        """Atualiza apenas o status de uma matéria."""
        query = "UPDATE materia SET status = %s WHERE id_materia = %s;"

        with self.conn.cursor() as cursor:
            cursor.execute(query, (novo_status, id_materia))
            self.conn.commit()
            return cursor.rowcount > 0

    def alocar_editor_chefe(
        self,
        id_materia: int,
        editor_chefe_cpf: str
    ) -> bool:
        """Aloca ou altera o editor chefe de uma matéria."""
        query = "UPDATE materia SET cpf_editor_chefe = %s WHERE id_materia = %s;"

        with self.conn.cursor() as cursor:
            cursor.execute(query, (editor_chefe_cpf, id_materia))
            self.conn.commit()
            return cursor.rowcount > 0

    def vincular_jornalista(
        self,
        materia_id: int,
        jornalista_cpf: str,
        papel: str = "Autor Principal"
    ) -> bool:
        """Vincula um jornalista a uma matéria na tabela associativa."""
        query = """
            INSERT INTO materia_jornalista (materia_id, jornalista_cpf, papel)
            VALUES (%s, %s, %s)
            ON CONFLICT (materia_id, jornalista_cpf)
            DO UPDATE SET papel = EXCLUDED.papel;
        """

        with self.conn.cursor() as cursor:
            cursor.execute(
                query,
                (materia_id, jornalista_cpf, papel)
            )
            self.conn.commit()
            return True

    def desvincular_jornalista(
        self,
        materia_id: int,
        jornalista_cpf: str
    ) -> bool:
        """Remove o vínculo de um jornalista com uma matéria."""
        query = """
            DELETE FROM materia_jornalista
            WHERE materia_id = %s AND jornalista_cpf = %s;
        """

        with self.conn.cursor() as cursor:
            cursor.execute(
                query,
                (materia_id, jornalista_cpf)
            )
            self.conn.commit()
            return cursor.rowcount > 0
        
    def listar_jornalistas(
        self,
        materia_id: int
    ) -> List[Dict[str, Any]]:
        """Lista os jornalistas vinculados a uma matéria."""
        query = """
            SELECT
                cpf_jornalista
            FROM alocacao_jornalista_materia
            WHERE id_materia = %s
            ORDER BY cpf_jornalista;
        """

        with self.conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                query,
                (materia_id,)
            )
            return cursor.fetchall()

    def deletar(self, id_materia: int) -> bool:
        """Remove uma matéria do banco de dados pelo ID."""
        query = "DELETE FROM materia WHERE id_materia = %s;"

        with self.conn.cursor() as cursor:
            cursor.execute(query, (id_materia,))
            self.conn.commit()
            return cursor.rowcount > 0