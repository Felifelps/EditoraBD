from psycopg import Connection
from psycopg.rows import class_row

from app.schemas.funcionario import Funcionario, FuncionarioCreate, FuncionarioUpdate

COLUNAS = "cpf, nome, rua, cep, numero, data_nascimento, email, telefone, salario, tipo"


class FuncionarioRepository:
    def __init__(self, conn: Connection):
        self.conn = conn

    def listar_todos(self) -> list[Funcionario]:
        with self.conn.cursor(row_factory=class_row(Funcionario)) as cur:
            cur.execute(f"SELECT {COLUNAS} FROM funcionario ORDER BY nome")
            return cur.fetchall()

    def buscar_por_cpf(self, cpf: str) -> Funcionario | None:
        with self.conn.cursor(row_factory=class_row(Funcionario)) as cur:
            cur.execute(f"SELECT {COLUNAS} FROM funcionario WHERE cpf = %s", (cpf,))
            return cur.fetchone()

    def criar(self, dados: FuncionarioCreate) -> Funcionario:
        with self.conn.cursor(row_factory=class_row(Funcionario)) as cur:
            cur.execute(
                f"""
                INSERT INTO funcionario
                    (cpf, nome, rua, cep, numero, data_nascimento, email, telefone, salario, tipo)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING {COLUNAS}
                """,
                (
                    dados.cpf,
                    dados.nome,
                    dados.rua,
                    dados.cep,
                    dados.numero,
                    dados.data_nascimento,
                    dados.email,
                    dados.telefone,
                    dados.salario,
                    dados.tipo,
                ),
            )
            return cur.fetchone()

    def atualizar(self, cpf: str, dados: FuncionarioUpdate) -> Funcionario | None:
        with self.conn.cursor(row_factory=class_row(Funcionario)) as cur:
            cur.execute(
                f"""
                UPDATE funcionario
                SET nome = %s, rua = %s, cep = %s, numero = %s, data_nascimento = %s,
                    email = %s, telefone = %s, salario = %s, tipo = %s
                WHERE cpf = %s
                RETURNING {COLUNAS}
                """,
                (
                    dados.nome,
                    dados.rua,
                    dados.cep,
                    dados.numero,
                    dados.data_nascimento,
                    dados.email,
                    dados.telefone,
                    dados.salario,
                    dados.tipo,
                    cpf,
                ),
            )
            return cur.fetchone()

    def deletar(self, cpf: str) -> bool:
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM funcionario WHERE cpf = %s", (cpf,))
            return cur.rowcount > 0
