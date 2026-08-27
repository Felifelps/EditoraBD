from psycopg import Connection
from psycopg.rows import dict_row


class RelatorioRepository:
    def __init__(self, conn: Connection):
        self.conn = conn

    def resumo_edicoes_jornal(self) -> list[dict]:
        return self._buscar(
            """
            SELECT nome_jornal, nome_diretor, total_edicoes, ultima_edicao
            FROM vw_resumo_edicoes_jornal
            ORDER BY nome_jornal
            """
        )

    def carga_materias_jornalista(self) -> list[dict]:
        return self._buscar(
            """
            SELECT cpf_jornalista, nome_jornalista, mtb, total_materias,
                   materias_aprovadas, materias_reprovadas, materias_em_andamento
            FROM vw_carga_materias_jornalista
            ORDER BY nome_jornalista
            """
        )

    def setores_editores(self) -> list[dict]:
        return self._buscar(
            """
            SELECT id_setor, nome_setor, descricao_setor, cpf_editor_chefe,
                   nome_editor, especialidades
            FROM vw_setores_editores
            ORDER BY nome_setor
            """
        )

    def funcionarios_detalhes(self) -> list[dict]:
        return self._buscar(
            """
            SELECT cpf, nome, email, telefone, salario, data_inicio_mandato,
                   mtb, cargo
            FROM vw_funcionarios_detalhes
            ORDER BY nome
            """
        )

    def materias_completas(self) -> list[dict]:
        return self._buscar(
            """
            SELECT id_materia, titulo, data_materia, status_texto, nome_setor,
                   numero_edicao, nome_jornal, autores
            FROM vw_materias_completas
            ORDER BY data_materia DESC, titulo
            """
        )

    def historico_status_materia(self) -> list[dict]:
        return self._buscar(
            """
            SELECT id, id_materia, titulo, status_anterior_texto,
                   status_novo_texto, alterado_em
            FROM vw_historico_status_materia
            ORDER BY alterado_em DESC
            """
        )

    def _buscar(self, query: str) -> list[dict]:
        with self.conn.cursor(row_factory=dict_row) as cur:
            cur.execute(query)
            return cur.fetchall()