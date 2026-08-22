from psycopg import Connection
from psycopg.rows import class_row

from app.schemas.jornal import Jornal, JornalCreate, JornalUpdate

SELECT_COM_DIRETOR = """
    SELECT j.nome_jornal, j.cpf_diretor, f.nome AS nome_diretor
    FROM jornal j
    LEFT JOIN funcionario f ON f.cpf = j.cpf_diretor
"""


class JornalRepository:
    def __init__(self, conn: Connection):
        self.conn = conn

    def listar_todos(self) -> list[Jornal]:
        with self.conn.cursor(row_factory=class_row(Jornal)) as cur:
            cur.execute(f"{SELECT_COM_DIRETOR} ORDER BY j.nome_jornal")
            return cur.fetchall()

    def buscar_por_nome(self, nome_jornal: str) -> Jornal | None:
        with self.conn.cursor(row_factory=class_row(Jornal)) as cur:
            cur.execute(f"{SELECT_COM_DIRETOR} WHERE j.nome_jornal = %s", (nome_jornal,))
            return cur.fetchone()

    def listar_diretores(self) -> list[dict]:
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT f.cpf, f.nome
                FROM diretor d
                JOIN funcionario f ON f.cpf = d.cpf_diretor
                ORDER BY f.nome
                """
            )
            return [{"cpf": cpf, "nome": nome} for cpf, nome in cur.fetchall()]

    def criar(self, dados: JornalCreate) -> Jornal:
        self.conn.execute(
            "INSERT INTO jornal (nome_jornal, cpf_diretor) VALUES (%s, %s)",
            (dados.nome_jornal, dados.cpf_diretor),
        )
        return self.buscar_por_nome(dados.nome_jornal)

    def atualizar(self, nome_jornal: str, dados: JornalUpdate) -> Jornal | None:
        if self.buscar_por_nome(nome_jornal) is None:
            return None

        self.conn.execute(
            "UPDATE jornal SET cpf_diretor = %s WHERE nome_jornal = %s",
            (dados.cpf_diretor, nome_jornal),
        )
        return self.buscar_por_nome(nome_jornal)

    def deletar(self, nome_jornal: str) -> bool:
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM jornal WHERE nome_jornal = %s", (nome_jornal,))
            return cur.rowcount > 0
