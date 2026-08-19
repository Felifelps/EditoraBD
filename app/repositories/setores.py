from psycopg import Connection
from psycopg.rows import class_row

from app.schemas.setor import Setor, SetorCreate, SetorUpdate

SELECT_COM_EDITOR = """
    SELECT s.id_setor, s.nome, s.descricao, s.cpf_editor_chefe, f.nome AS nome_editor_chefe
    FROM setor s
    LEFT JOIN funcionario f ON f.cpf = s.cpf_editor_chefe
"""


class SetorRepository:
    def __init__(self, conn: Connection):
        self.conn = conn

    def listar_todos(self) -> list[Setor]:
        with self.conn.cursor(row_factory=class_row(Setor)) as cur:
            cur.execute(f"{SELECT_COM_EDITOR} ORDER BY s.nome")
            return cur.fetchall()

    def buscar_por_id(self, id_setor: int) -> Setor | None:
        with self.conn.cursor(row_factory=class_row(Setor)) as cur:
            cur.execute(f"{SELECT_COM_EDITOR} WHERE s.id_setor = %s", (id_setor,))
            return cur.fetchone()

    def listar_editores_chefe(self) -> list[dict]:
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT f.cpf, f.nome
                FROM editor_chefe e
                JOIN funcionario f ON f.cpf = e.cpf_editor
                ORDER BY f.nome
                """
            )
            return [{"cpf": cpf, "nome": nome} for cpf, nome in cur.fetchall()]

    def criar(self, dados: SetorCreate) -> Setor:
        self.conn.execute(
            "INSERT INTO setor (id_setor, nome, descricao, cpf_editor_chefe) VALUES (%s, %s, %s, %s)",
            (dados.id_setor, dados.nome, dados.descricao, dados.cpf_editor_chefe),
        )
        return self.buscar_por_id(dados.id_setor)

    def atualizar(self, id_setor: int, dados: SetorUpdate) -> Setor | None:
        if self.buscar_por_id(id_setor) is None:
            return None

        self.conn.execute(
            "UPDATE setor SET nome = %s, descricao = %s, cpf_editor_chefe = %s WHERE id_setor = %s",
            (dados.nome, dados.descricao, dados.cpf_editor_chefe, id_setor),
        )
        return self.buscar_por_id(id_setor)

    def deletar(self, id_setor: int) -> bool:
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM setor WHERE id_setor = %s", (id_setor,))
            return cur.rowcount > 0
