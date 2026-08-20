from fastapi import Depends
from psycopg import Connection

from app.db.dependencies import get_conn
from app.exceptions.setores import SetorJaExisteError, SetorNaoEncontradoError
from app.repositories.setores import SetorRepository
from app.schemas.setor import Setor, SetorCreate, SetorUpdate


class SetorService:
    def __init__(self, repo: SetorRepository):
        self.repo = repo

    def listar(self) -> list[Setor]:
        return self.repo.listar_todos()

    def buscar(self, id_setor: int) -> Setor | None:
        return self.repo.buscar_por_id(id_setor)

    def listar_editores_chefe(self) -> list[dict]:
        return self.repo.listar_editores_chefe()

    def criar(self, dados: SetorCreate) -> Setor:
        if self.repo.buscar_por_id(dados.id_setor) is not None:
            raise SetorJaExisteError(f"Ja existe setor com id {dados.id_setor}")

        return self.repo.criar(dados)

    def atualizar(self, id_setor: int, dados: SetorUpdate) -> Setor:
        setor = self.repo.atualizar(id_setor, dados)

        if setor is None:
            raise SetorNaoEncontradoError(f"Setor {id_setor} nao encontrado")

        return setor

    def deletar(self, id_setor: int) -> None:
        if not self.repo.deletar(id_setor):
            raise SetorNaoEncontradoError(f"Setor {id_setor} nao encontrado")


def get_setor_service(conn: Connection = Depends(get_conn)) -> SetorService:
    return SetorService(SetorRepository(conn))
