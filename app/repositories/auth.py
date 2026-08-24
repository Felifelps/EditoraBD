from psycopg import Connection
from psycopg.rows import dict_row


class AuthRepository:
    def __init__(self, conn: Connection):
        self.conn = conn

    def buscar_por_email(self, email: str) -> dict | None:
        with self.conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                "SELECT cpf, nome, email, senha_hash FROM funcionario WHERE email = %s",
                (email,),
            )
            return cur.fetchone()
