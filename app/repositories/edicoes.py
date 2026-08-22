from psycopg import Connection
from psycopg.rows import class_row

from app.schemas.edicao import Edicao, EdicaoCreate, EdicaoUpdate

SELECT_EDICAO = """
    SELECT nome_jornal, numero_edicao, data
    FROM edicao
"""


class EdicaoRepository:
    def __init__(self, conn: Connection):
        self.conn = conn

    def listar_todas(self) -> list[Edicao]:
        with self.conn.cursor(row_factory=class_row(Edicao)) as cur:
            cur.execute(f"{SELECT_EDICAO} ORDER BY nome_jornal, numero_edicao")
            return cur.fetchall()

    def buscar(self, nome_jornal: str, numero_edicao: int) -> Edicao | None:
        with self.conn.cursor(row_factory=class_row(Edicao)) as cur:
            cur.execute(
                f"{SELECT_EDICAO} WHERE nome_jornal = %s AND numero_edicao = %s",
                (nome_jornal, numero_edicao),
            )
            return cur.fetchone()

    def listar_jornais(self) -> list[str]:
        with self.conn.cursor() as cur:
            cur.execute("SELECT nome_jornal FROM jornal ORDER BY nome_jornal")
            return [nome for (nome,) in cur.fetchall()]

    def criar(self, dados: EdicaoCreate) -> Edicao:
        self.conn.execute(
            "INSERT INTO edicao (nome_jornal, numero_edicao, data) VALUES (%s, %s, %s)",
            (dados.nome_jornal, dados.numero_edicao, dados.data),
        )
        return self.buscar(dados.nome_jornal, dados.numero_edicao)

    def atualizar(self, nome_jornal: str, numero_edicao: int, dados: EdicaoUpdate) -> Edicao | None:
        if self.buscar(nome_jornal, numero_edicao) is None:
            return None

        self.conn.execute(
            "UPDATE edicao SET data = %s WHERE nome_jornal = %s AND numero_edicao = %s",
            (dados.data, nome_jornal, numero_edicao),
        )
        return self.buscar(nome_jornal, numero_edicao)

    def deletar(self, nome_jornal: str, numero_edicao: int) -> bool:
        with self.conn.cursor() as cur:
            cur.execute(
                "DELETE FROM edicao WHERE nome_jornal = %s AND numero_edicao = %s",
                (nome_jornal, numero_edicao),
            )
            return cur.rowcount > 0
