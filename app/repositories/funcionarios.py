from psycopg import Connection
from psycopg.rows import class_row

from app.schemas.funcionario import FuncionarioAuth, UsuarioSessao


def buscar_por_email(conn: Connection, email: str) -> FuncionarioAuth | None:
    with conn.cursor(row_factory=class_row(FuncionarioAuth)) as cur:
        cur.execute(
            "SELECT cpf, nome, email, senha_hash, tipo FROM funcionario WHERE email = %s",
            (email,),
        )
        return cur.fetchone()


def buscar_por_cpf(conn: Connection, cpf: str) -> UsuarioSessao | None:
    with conn.cursor(row_factory=class_row(UsuarioSessao)) as cur:
        cur.execute(
            "SELECT cpf, nome, email, tipo FROM funcionario WHERE cpf = %s",
            (cpf,),
        )
        return cur.fetchone()
