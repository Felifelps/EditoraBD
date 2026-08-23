from psycopg import Connection
from psycopg.rows import class_row

from app.schemas.funcionario import Funcionario, FuncionarioCreate, FuncionarioUpdate

# "tipo" nao e coluna de funcionario: e derivado de qual subtabela
# (diretor/jornalista/editor_chefe) contem o CPF, conforme a especializacao do esquema.
# editor_chefe especializa jornalista (nao funcionario diretamente), entao um CPF la
# tambem existe em jornalista; a checagem de editor_chefe vem antes para reportar o
# tipo mais especifico.
SELECT_COM_TIPO = """
    SELECT f.cpf, f.nome, f.rua, f.cep, f.numero, f.data_nascimento,
           f.email, f.telefone, f.salario,
           CASE
               WHEN d.cpf_diretor IS NOT NULL THEN 'diretor'
               WHEN e.cpf_editor IS NOT NULL THEN 'editor_chefe'
               WHEN j.cpf_jornalista IS NOT NULL THEN 'jornalista'
           END AS tipo
    FROM funcionario f
    LEFT JOIN diretor d ON d.cpf_diretor = f.cpf
    LEFT JOIN jornalista j ON j.cpf_jornalista = f.cpf
    LEFT JOIN editor_chefe e ON e.cpf_editor = f.cpf
"""


class FuncionarioRepository:
    def __init__(self, conn: Connection):
        self.conn = conn

    def listar_todos(self) -> list[Funcionario]:
        with self.conn.cursor(row_factory=class_row(Funcionario)) as cur:
            cur.execute(f"{SELECT_COM_TIPO} ORDER BY f.nome")
            return cur.fetchall()

    def buscar_por_cpf(self, cpf: str) -> Funcionario | None:
        with self.conn.cursor(row_factory=class_row(Funcionario)) as cur:
            cur.execute(f"{SELECT_COM_TIPO} WHERE f.cpf = %s", (cpf,))
            return cur.fetchone()

    def _definir_tipo(self, cpf: str, tipo: str) -> None:
        """Move o CPF para a subtabela de especializacao correta, removendo-o das demais.

        editor_chefe especializa jornalista (nao funcionario diretamente): definir
        tipo="editor_chefe" exige que a linha em jornalista exista antes do insert em
        editor_chefe, por causa da FK encadeada.
        """
        self.conn.execute("DELETE FROM diretor WHERE cpf_diretor = %s", (cpf,))

        if tipo == "diretor":
            self.conn.execute("DELETE FROM jornalista WHERE cpf_jornalista = %s", (cpf,))
            self.conn.execute(
                "INSERT INTO diretor (cpf_diretor) VALUES (%s) ON CONFLICT DO NOTHING", (cpf,)
            )
            return

        self.conn.execute(
            "INSERT INTO jornalista (cpf_jornalista) VALUES (%s) ON CONFLICT DO NOTHING", (cpf,)
        )
        if tipo == "editor_chefe":
            self.conn.execute(
                "INSERT INTO editor_chefe (cpf_editor) VALUES (%s) ON CONFLICT DO NOTHING", (cpf,)
            )
        else:
            self.conn.execute("DELETE FROM editor_chefe WHERE cpf_editor = %s", (cpf,))

    def criar(self, dados: FuncionarioCreate) -> Funcionario:
        with self.conn.transaction():
            self.conn.execute(
                """
                INSERT INTO funcionario
                    (cpf, nome, rua, cep, numero, data_nascimento, email, telefone, salario)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
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
                ),
            )
            self._definir_tipo(dados.cpf, dados.tipo)
        return self.buscar_por_cpf(dados.cpf)

    def atualizar(self, cpf: str, dados: FuncionarioUpdate) -> Funcionario | None:
        if self.buscar_por_cpf(cpf) is None:
            return None

        with self.conn.transaction():
            self.conn.execute(
                """
                UPDATE funcionario
                SET nome = %s, rua = %s, cep = %s, numero = %s, data_nascimento = %s,
                    email = %s, telefone = %s, salario = %s
                WHERE cpf = %s
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
                    cpf,
                ),
            )
            self._definir_tipo(cpf, dados.tipo)
        return self.buscar_por_cpf(cpf)

    def deletar(self, cpf: str) -> bool:
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM funcionario WHERE cpf = %s", (cpf,))
            return cur.rowcount > 0
