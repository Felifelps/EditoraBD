from fastapi import Depends
from psycopg import Connection

from app.db.dependencies import get_conn
from app.exceptions.jornais import JornalJaExisteError, JornalNaoEncontradoError
from app.repositories.jornais import JornalRepository
from app.schemas.jornal import Jornal, JornalCreate, JornalUpdate


class JornalService:
    def __init__(self, repo: JornalRepository):
        self.repo = repo

    def listar(self) -> list[Jornal]:
        return self.repo.listar_todos()

    def buscar(self, nome_jornal: str) -> Jornal | None:
        return self.repo.buscar_por_nome(nome_jornal)

    def listar_diretores(self) -> list[dict]:
        return self.repo.listar_diretores()

    def criar(self, dados: JornalCreate) -> Jornal:
        if self.repo.buscar_por_nome(dados.nome_jornal) is not None:
            raise JornalJaExisteError(f"Ja existe jornal com nome {dados.nome_jornal}")

        return self.repo.criar(dados)

    def atualizar(self, nome_jornal: str, dados: JornalUpdate) -> Jornal:
        jornal = self.repo.atualizar(nome_jornal, dados)

        if jornal is None:
            raise JornalNaoEncontradoError(f"Jornal {nome_jornal} nao encontrado")

        return jornal

    def deletar(self, nome_jornal: str) -> None:
        if not self.repo.deletar(nome_jornal):
            raise JornalNaoEncontradoError(f"Jornal {nome_jornal} nao encontrado")


def get_jornal_service(conn: Connection = Depends(get_conn)) -> JornalService:
    return JornalService(JornalRepository(conn))
