from typing import Any, Dict, List
from fastapi import Depends
from psycopg import Connection

from app.db.dependencies import get_conn
from app.exceptions.materias import MateriaJaExisteError, MateriaNaoEncontradaError
from app.repositories.materias import MateriaRepository
from app.schemas.materias import MateriaAtualizar, MateriaCriar


class MateriaService:
    def __init__(self, repo: MateriaRepository):
        self.repo = repo

    def listar(
        self, 
        search: str | None = None, 
        status: int | None = None, 
        setor_id: int | None = None
    ) -> list[dict[str, Any]]:
        return self.repo.listar_todas(search=search, status=status, setor_id=setor_id)

    def obter_por_id(self, id_materia: int) -> dict[str, Any] | None:
        materia = self.repo.buscar_por_id(id_materia)
        if materia is None:
            raise MateriaNaoEncontradaError(f"Matéria com ID {id_materia} não encontrada")
        return materia

    def criar(self, dados: MateriaCriar) -> dict[str, Any]:
        return self.repo.criar(dados)

    def atualizar(self, id_materia: int, dados: MateriaAtualizar) -> dict[str, Any]:
        materia = self.repo.atualizar(id_materia, dados)
        if materia is None:
            raise MateriaNaoEncontradaError(f"Matéria com ID {id_materia} não encontrada")
        return materia

    def atualizar_status(self, id_materia: int, novo_status: int) -> None:
        if not self.repo.atualizar_status(id_materia, novo_status):
            raise MateriaNaoEncontradaError(f"Matéria com ID {id_materia} não encontrada")

    def alocar_editor_chefe(self, id_materia: int, editor_chefe_cpf: str) -> None:
        if not self.repo.alocar_editor_chefe(id_materia, editor_chefe_cpf):
            raise MateriaNaoEncontradaError(f"Matéria com ID {id_materia} não encontrada")

    def vincular_jornalista(self, materia_id: int, jornalista_cpf: str, papel: str = "Autor Principal") -> None:
        if not self.repo.vincular_jornalista(materia_id, jornalista_cpf, papel):
            raise MateriaNaoEncontradaError(f"Matéria com ID {materia_id} não encontrada")

    def desvincular_jornalista(self, materia_id: int, jornalista_cpf: str) -> None:
        self.repo.desvincular_jornalista(materia_id, jornalista_cpf)

    def deletar(self, id_materia: int) -> None:
        if not self.repo.deletar(id_materia):
            raise MateriaNaoEncontradaError(f"Matéria com ID {id_materia} não encontrada")


def get_materia_service(conn: Connection = Depends(get_conn)) -> MateriaService:
    return MateriaService(MateriaRepository(conn))