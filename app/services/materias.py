from typing import Any

from fastapi import Depends
from psycopg import Connection

from app.db.dependencies import get_conn
from app.exceptions.materias import (
    MateriaJaExisteError,
    MateriaNaoEncontradaError,
)
from app.repositories.materias import MateriaRepository
from app.schemas.materias import MateriaAtualizar, MateriaCriar


class MateriaService:

    def __init__(self, repo: MateriaRepository):
        self.repo = repo

    def listar(
        self,
        search: str | None = None,
        status: int | None = None,
        setor_id: int | None = None,
    ) -> list[dict[str, Any]]:
        return self.repo.listar_todas(
            search=search,
            status=status,
            setor_id=setor_id,
        )

    def obter_por_id(
        self,
        id_materia: int,
    ) -> dict[str, Any]:
        materia = self.repo.buscar_por_id(id_materia)

        if materia is None:
            raise MateriaNaoEncontradaError(
                f"Matéria com ID {id_materia} não encontrada"
            )

        return materia

    def criar(
        self,
        dados: MateriaCriar,
    ) -> dict[str, Any]:
        duplicada = self.repo.buscar_duplicada(
            titulo=dados.titulo,
            data=dados.data,
            nome_jornal=dados.nome_jornal,
            numero_edicao=dados.numero_edicao,
            id_setor=dados.id_setor,
        )

        if duplicada is not None:
            raise MateriaJaExisteError(
                "Já existe uma matéria com o mesmo "
                "título, data, jornal, edição e setor."
            )

        return self.repo.criar(
            dados.model_dump()
        )

    def atualizar(
        self,
        id_materia: int,
        dados: MateriaAtualizar,
    ) -> dict[str, Any]:
        self.obter_por_id(id_materia)

        duplicada = self.repo.buscar_duplicada(
            titulo=dados.titulo,
            data=dados.data,
            nome_jornal=dados.nome_jornal,
            numero_edicao=dados.numero_edicao,
            id_setor=dados.id_setor,
            id_materia=id_materia,
        )

        if duplicada is not None:
            raise MateriaJaExisteError(
                "Já existe outra matéria com os mesmos "
                "dados."
            )

        materia = self.repo.atualizar(
            id_materia,
            dados.model_dump(),
        )

        if materia is None:
            raise MateriaNaoEncontradaError(
                f"Matéria com ID {id_materia} não encontrada"
            )

        return materia

    def atualizar_status(
        self,
        id_materia: int,
        novo_status: int,
    ) -> None:
        self.obter_por_id(id_materia)

        self.repo.atualizar_status(
            id_materia,
            novo_status,
        )

    def deletar(
        self,
        id_materia: int,
    ) -> None:
        self.obter_por_id(id_materia)

        self.repo.deletar(id_materia)

    def listar_jornalistas(
        self,
        materia_id: int,
    ) -> list[dict[str, Any]]:
        self.obter_por_id(materia_id)

        return self.repo.listar_jornalistas(
            materia_id
        )

    def vincular_jornalista(
        self,
        materia_id: int,
        jornalista_cpf: str,
    ) -> None:
        self.obter_por_id(materia_id)

        self.repo.vincular_jornalista(
            materia_id,
            jornalista_cpf,
        )

    def desvincular_jornalista(
        self,
        materia_id: int,
        jornalista_cpf: str,
    ) -> None:
        self.obter_por_id(materia_id)

        self.repo.desvincular_jornalista(
            materia_id,
            jornalista_cpf,
        )


def get_materia_service(
    conn: Connection = Depends(get_conn),
) -> MateriaService:
    return MateriaService(
        MateriaRepository(conn)
    )