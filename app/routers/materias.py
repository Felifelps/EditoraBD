from datetime import date

from fastapi import (
    APIRouter,
    Depends,
    Form,
    HTTPException,
    Query,
    Request,
)
from fastapi.responses import RedirectResponse
from pydantic import ValidationError

from app.exceptions.materias import MateriaNaoEncontradaError
from app.schemas.materias import MateriaAtualizar, MateriaCriar
from app.services.edicoes import EdicaoService, get_edicao_service
from app.services.funcionarios import (
    FuncionarioService,
    get_funcionario_service,
)
from app.services.jornais import JornalService, get_jornal_service
from app.services.materias import MateriaService, get_materia_service
from app.services.setores import SetorService, get_setor_service
from app.templating import templates


router = APIRouter(prefix="/materias")


@router.get("")
def listar(
    request: Request,
    search: str | None = Query(None),
    status: int | None = Query(None),
    setor_id: int | None = Query(None),
    service: MateriaService = Depends(get_materia_service),
    setor_service: SetorService = Depends(get_setor_service),
):
    return templates.TemplateResponse(
        request,
        "materias/list.html",
        {
            "materias": service.listar(
                search=search,
                status=status,
                setor_id=setor_id,
            ),
            "setores": setor_service.listar(),
            "search": search or "",
            "status": status,
            "setor_id": setor_id,
        },
    )


@router.get("/novo")
def form_novo(
    request: Request,
    setor_service: SetorService = Depends(get_setor_service),
    jornal_service: JornalService = Depends(get_jornal_service),
    edicao_service: EdicaoService = Depends(get_edicao_service),
):
    return templates.TemplateResponse(
        request,
        "materias/form.html",
        {
            "erro": None,
            "materia": None,
            "acao": "/materias/novo",
            "setores": setor_service.listar(),
            "jornais": jornal_service.listar(),
            "edicoes": edicao_service.listar(),
        },
    )


@router.post("/novo")
def criar(
    request: Request,
    titulo: str = Form(...),
    subtitulo: str = Form(""),
    resumo: str = Form(""),
    conteudo: str = Form(...),
    data: str = Form(...),
    status: int = Form(...),
    nome_jornal: str = Form(""),
    numero_edicao: int | None = Form(None),
    id_setor: int | None = Form(None),
    service: MateriaService = Depends(get_materia_service),
    setor_service: SetorService = Depends(get_setor_service),
    jornal_service: JornalService = Depends(get_jornal_service),
    edicao_service: EdicaoService = Depends(get_edicao_service),
):
    try:
        dados = MateriaCriar(
            titulo=titulo,
            subtitulo=subtitulo or None,
            resumo=resumo or None,
            conteudo=conteudo,
            data=date.fromisoformat(data),
            status=status,
            nome_jornal=nome_jornal or None,
            numero_edicao=numero_edicao,
            id_setor=id_setor,
        )

        service.criar(dados)

    except (ValueError, ValidationError) as exc:
        return templates.TemplateResponse(
            request,
            "materias/form.html",
            {
                "erro": str(exc),
                "materia": None,
                "acao": "/materias/novo",
                "setores": setor_service.listar(),
                "jornais": jornal_service.listar(),
                "edicoes": edicao_service.listar(),
            },
            status_code=400,
        )

    return RedirectResponse(
        url="/materias",
        status_code=303,
    )


@router.get("/{id_materia}")
def detalhar(
    request: Request,
    id_materia: int,
    service: MateriaService = Depends(get_materia_service),
    funcionario_service: FuncionarioService = Depends(
        get_funcionario_service
    ),
):
    try:
        materia = service.obter_por_id(id_materia)
        alocados = service.listar_jornalistas(id_materia)
    except MateriaNaoEncontradaError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    funcionarios = funcionario_service.listar()

    todos_jornalistas = [
        funcionario
        for funcionario in funcionarios
        if getattr(
            funcionario,
            "tipo",
            None,
        ) == "jornalista"
    ]

    jornalistas = []

    for alocado in alocados:
        cpf = alocado["cpf_jornalista"]

        jornalista = next(
            (
                funcionario
                for funcionario in todos_jornalistas
                if funcionario.cpf == cpf
            ),
            None,
        )

        jornalistas.append(
            {
                "cpf": cpf,
                "nome": (
                    jornalista.nome
                    if jornalista
                    else cpf
                ),
            }
        )

    return templates.TemplateResponse(
        request,
        "materias/detail.html",
        {
            "materia": materia,
            "jornalistas": jornalistas,
            "todos_jornalistas": todos_jornalistas,
        },
    )


@router.get("/{id_materia}/editar")
def form_editar(
    request: Request,
    id_materia: int,
    service: MateriaService = Depends(get_materia_service),
    setor_service: SetorService = Depends(get_setor_service),
    jornal_service: JornalService = Depends(get_jornal_service),
    edicao_service: EdicaoService = Depends(get_edicao_service),
):
    try:
        materia = service.obter_por_id(id_materia)
    except MateriaNaoEncontradaError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    return templates.TemplateResponse(
        request,
        "materias/form.html",
        {
            "erro": None,
            "materia": materia,
            "acao": f"/materias/{id_materia}/editar",
            "setores": setor_service.listar(),
            "jornais": jornal_service.listar(),
            "edicoes": edicao_service.listar(),
        },
    )


@router.post("/{id_materia}/editar")
def atualizar(
    request: Request,
    id_materia: int,
    titulo: str = Form(...),
    subtitulo: str = Form(""),
    resumo: str = Form(""),
    conteudo: str = Form(...),
    data: str = Form(...),
    status: int = Form(...),
    nome_jornal: str = Form(""),
    numero_edicao: int | None = Form(None),
    id_setor: int | None = Form(None),
    service: MateriaService = Depends(get_materia_service),
    setor_service: SetorService = Depends(get_setor_service),
    jornal_service: JornalService = Depends(get_jornal_service),
    edicao_service: EdicaoService = Depends(get_edicao_service),
):
    try:
        dados = MateriaAtualizar(
            titulo=titulo,
            subtitulo=subtitulo or None,
            resumo=resumo or None,
            conteudo=conteudo,
            data=date.fromisoformat(data),
            status=status,
            nome_jornal=nome_jornal or None,
            numero_edicao=numero_edicao,
            id_setor=id_setor,
        )

        service.atualizar(
            id_materia,
            dados,
        )

    except MateriaNaoEncontradaError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    except (ValueError, ValidationError) as exc:
        try:
            materia = service.obter_por_id(id_materia)
        except MateriaNaoEncontradaError as materia_exc:
            raise HTTPException(
                status_code=404,
                detail=str(materia_exc),
            ) from materia_exc

        return templates.TemplateResponse(
            request,
            "materias/form.html",
            {
                "erro": str(exc),
                "materia": materia,
                "acao": f"/materias/{id_materia}/editar",
                "setores": setor_service.listar(),
                "jornais": jornal_service.listar(),
                "edicoes": edicao_service.listar(),
            },
            status_code=400,
        )

    return RedirectResponse(
        url=f"/materias/{id_materia}",
        status_code=303,
    )


@router.post("/{id_materia}/deletar")
def deletar(
    id_materia: int,
    service: MateriaService = Depends(get_materia_service),
):
    try:
        service.deletar(id_materia)
    except MateriaNaoEncontradaError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    return RedirectResponse(
        url="/materias",
        status_code=303,
    )


@router.post("/{id_materia}/jornalistas/alocar")
def alocar_jornalista(
    id_materia: int,
    cpf_jornalista: str = Form(...),
    service: MateriaService = Depends(get_materia_service),
    funcionario_service: FuncionarioService = Depends(
        get_funcionario_service
    ),
):
    try:
        service.obter_por_id(id_materia)
    except MateriaNaoEncontradaError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    funcionarios = funcionario_service.listar()

    jornalista = next(
        (
            funcionario
            for funcionario in funcionarios
            if getattr(
                funcionario,
                "cpf",
                None,
            ) == cpf_jornalista
            and getattr(
                funcionario,
                "tipo",
                None,
            ) == "jornalista"
        ),
        None,
    )

    if jornalista is None:
        raise HTTPException(
            status_code=400,
            detail="O CPF informado não pertence a um jornalista.",
        )

    try:
        service.vincular_jornalista(
            id_materia,
            cpf_jornalista,
        )
    except MateriaNaoEncontradaError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    return RedirectResponse(
        url=f"/materias/{id_materia}",
        status_code=303,
    )


@router.post(
    "/{id_materia}/jornalistas/"
    "{cpf_jornalista}/deletar"
)
def desalocar_jornalista(
    id_materia: int,
    cpf_jornalista: str,
    service: MateriaService = Depends(get_materia_service),
):
    try:
        service.desvincular_jornalista(
            id_materia,
            cpf_jornalista,
        )
    except MateriaNaoEncontradaError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    return RedirectResponse(
        url=f"/materias/{id_materia}",
        status_code=303,
    )