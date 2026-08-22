from fastapi import Depends
from psycopg import Connection

from app.db.dependencies import get_conn
from app.exceptions.edicoes import EdicaoJaExisteError, EdicaoNaoEncontradaError
from app.repositories.edicoes import EdicaoRepository
from app.schemas.edicao import Edicao, EdicaoCreate, EdicaoUpdate


class EdicaoService:
    def __init__(self, repo: EdicaoRepository):
        self.repo = repo

    def listar(self) -> list[Edicao]:
        return self.repo.listar_todas()

    def buscar(self, nome_jornal: str, numero_edicao: int) -> Edicao | None:
        return self.repo.buscar(nome_jornal, numero_edicao)

    def listar_jornais(self) -> list[str]:
        return self.repo.listar_jornais()

    def criar(self, dados: EdicaoCreate) -> Edicao:
        if self.repo.buscar(dados.nome_jornal, dados.numero_edicao) is not None:
            raise EdicaoJaExisteError(
                f"Ja existe edicao {dados.numero_edicao} para o jornal {dados.nome_jornal}"
            )

        return self.repo.criar(dados)

    def atualizar(self, nome_jornal: str, numero_edicao: int, dados: EdicaoUpdate) -> Edicao:
        edicao = self.repo.atualizar(nome_jornal, numero_edicao, dados)

        if edicao is None:
            raise EdicaoNaoEncontradaError(f"Edicao {numero_edicao} de {nome_jornal} nao encontrada")

        return edicao

    def deletar(self, nome_jornal: str, numero_edicao: int) -> None:
        if not self.repo.deletar(nome_jornal, numero_edicao):
            raise EdicaoNaoEncontradaError(f"Edicao {numero_edicao} de {nome_jornal} nao encontrada")


def get_edicao_service(conn: Connection = Depends(get_conn)) -> EdicaoService:
    return EdicaoService(EdicaoRepository(conn))
