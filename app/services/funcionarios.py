from fastapi import Depends
from psycopg import Connection

from app.db.dependencies import get_conn
from app.exceptions.funcionarios import FuncionarioJaExisteError, FuncionarioNaoEncontradoError
from app.repositories.funcionarios import FuncionarioRepository
from app.schemas.funcionario import Funcionario, FuncionarioCreate, FuncionarioUpdate


class FuncionarioService:
    def __init__(self, repo: FuncionarioRepository):
        self.repo = repo

    def listar(self) -> list[Funcionario]:
        return self.repo.listar_todos()

    def buscar(self, cpf: str) -> Funcionario | None:
        return self.repo.buscar_por_cpf(cpf)

    def criar(self, dados: FuncionarioCreate) -> Funcionario:
        if self.repo.buscar_por_cpf(dados.cpf) is not None:
            raise FuncionarioJaExisteError(f"Ja existe funcionario com CPF {dados.cpf}")

        return self.repo.criar(dados)

    def atualizar(self, cpf: str, dados: FuncionarioUpdate) -> Funcionario:
        funcionario = self.repo.atualizar(cpf, dados)

        if funcionario is None:
            raise FuncionarioNaoEncontradoError(f"Funcionario {cpf} nao encontrado")

        return funcionario

    def deletar(self, cpf: str) -> None:
        if not self.repo.deletar(cpf):
            raise FuncionarioNaoEncontradoError(f"Funcionario {cpf} nao encontrado")


def get_funcionario_service(conn: Connection = Depends(get_conn)) -> FuncionarioService:
    return FuncionarioService(FuncionarioRepository(conn))
