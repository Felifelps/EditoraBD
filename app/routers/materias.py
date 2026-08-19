from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, Query, status

from app.schemas.materias import MateriaAtualizar, MateriaCriar
from app.services.materias import (
    MateriaService,
    get_materia_service,
)


router = APIRouter(
    prefix="/materias",
    tags=["Matérias"],
)


@router.get(
    "/",
    response_model=List[Dict[str, Any]],
)
def listar_materias(
    search: Optional[str] = Query(
        None,
        description="Termo para buscar no título",
    ),
    status: Optional[int] = Query(
        None,
        description="Filtrar por status (0, 1, 2)",
    ),
    setor_id: Optional[int] = Query(
        None,
        description="Filtrar por ID do setor",
    ),
    service: MateriaService = Depends(
        get_materia_service
    ),
):
    return service.listar(
        search=search,
        status=status,
        setor_id=setor_id,
    )


@router.get(
    "/{id_materia}",
    response_model=Dict[str, Any],
)
def obter_materia(
    id_materia: int,
    service: MateriaService = Depends(
        get_materia_service
    ),
):
    return service.obter_por_id(
        id_materia
    )


@router.post(
    "/",
    response_model=Dict[str, Any],
    status_code=status.HTTP_201_CREATED,
)
def criar_materia(
    dados: MateriaCriar,
    service: MateriaService = Depends(
        get_materia_service
    ),
):
    return service.criar(
        dados
    )


@router.put(
    "/{id_materia}",
    response_model=Dict[str, Any],
)
def atualizar_materia(
    id_materia: int,
    dados: MateriaAtualizar,
    service: MateriaService = Depends(
        get_materia_service
    ),
):
    return service.atualizar(
        id_materia,
        dados,
    )


@router.delete(
    "/{id_materia}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def deletar_materia(
    id_materia: int,
    service: MateriaService = Depends(
        get_materia_service
    ),
):
    service.deletar(
        id_materia
    )

    return None

@router.get(
    "/{id_materia}/jornalistas",
    response_model=List[Dict[str, Any]],
)
def listar_jornalistas(
    id_materia: int,
    service: MateriaService = Depends(
        get_materia_service
    ),
):
    return service.listar_jornalistas(
        id_materia
    )


@router.post(
    "/{id_materia}/jornalistas",
    status_code=status.HTTP_204_NO_CONTENT,
)
def alocar_jornalista(
    id_materia: int,
    cpf_jornalista: str,
    service: MateriaService = Depends(
        get_materia_service
    ),
):
    service.vincular_jornalista(
        id_materia,
        cpf_jornalista,
    )

    return None


@router.delete(
    "/{id_materia}/jornalistas/{cpf_jornalista}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def desalocar_jornalista(
    id_materia: int,
    cpf_jornalista: str,
    service: MateriaService = Depends(
        get_materia_service
    ),
):
    service.desvincular_jornalista(
        id_materia,
        cpf_jornalista,
    )

    return None