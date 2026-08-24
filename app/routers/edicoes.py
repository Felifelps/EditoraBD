from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse

from app.exceptions.edicoes import EdicaoJaExisteError, EdicaoNaoEncontradaError
from app.schemas.edicao import EdicaoCreate, EdicaoUpdate
from app.services.auth import obter_usuario_logado
from app.services.edicoes import EdicaoService, get_edicao_service
from app.templating import templates

router = APIRouter(prefix="/edicoes", dependencies=[Depends(obter_usuario_logado)])


@router.get("")
def listar(request: Request, service: EdicaoService = Depends(get_edicao_service)):
    return templates.TemplateResponse(request, "edicoes/list.html", {"edicoes": service.listar()})


@router.get("/novo")
def form_novo(request: Request, service: EdicaoService = Depends(get_edicao_service)):
    return templates.TemplateResponse(
        request,
        "edicoes/form.html",
        {"erro": None, "edicao": None, "acao": "/edicoes/novo", "jornais": service.listar_jornais()},
    )


@router.post("/novo")
def criar(
    request: Request,
    nome_jornal: str = Form(...),
    numero_edicao: int = Form(...),
    data: str = Form(""),
    service: EdicaoService = Depends(get_edicao_service),
):
    dados = EdicaoCreate(nome_jornal=nome_jornal, numero_edicao=numero_edicao, data=data or None)
    try:
        service.criar(dados)
    except EdicaoJaExisteError as exc:
        return templates.TemplateResponse(
            request,
            "edicoes/form.html",
            {
                "erro": str(exc),
                "edicao": None,
                "acao": "/edicoes/novo",
                "jornais": service.listar_jornais(),
            },
            status_code=409,
        )
    return RedirectResponse(url="/edicoes", status_code=303)


@router.get("/{nome_jornal}/{numero_edicao}")
def detalhar(
    request: Request,
    nome_jornal: str,
    numero_edicao: int,
    service: EdicaoService = Depends(get_edicao_service),
):
    edicao = service.buscar(nome_jornal, numero_edicao)
    if edicao is None:
        raise HTTPException(status_code=404, detail="Edicao nao encontrada")
    return templates.TemplateResponse(request, "edicoes/detail.html", {"edicao": edicao})


@router.get("/{nome_jornal}/{numero_edicao}/editar")
def form_editar(
    request: Request,
    nome_jornal: str,
    numero_edicao: int,
    service: EdicaoService = Depends(get_edicao_service),
):
    edicao = service.buscar(nome_jornal, numero_edicao)
    if edicao is None:
        raise HTTPException(status_code=404, detail="Edicao nao encontrada")
    return templates.TemplateResponse(
        request,
        "edicoes/form.html",
        {
            "erro": None,
            "edicao": edicao,
            "acao": f"/edicoes/{nome_jornal}/{numero_edicao}/editar",
            "jornais": service.listar_jornais(),
        },
    )


@router.post("/{nome_jornal}/{numero_edicao}/editar")
def atualizar(
    request: Request,
    nome_jornal: str,
    numero_edicao: int,
    data: str = Form(""),
    service: EdicaoService = Depends(get_edicao_service),
):
    dados = EdicaoUpdate(data=data or None)
    try:
        service.atualizar(nome_jornal, numero_edicao, dados)
    except EdicaoNaoEncontradaError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return RedirectResponse(url=f"/edicoes/{nome_jornal}/{numero_edicao}", status_code=303)


@router.post("/{nome_jornal}/{numero_edicao}/deletar")
def deletar(
    nome_jornal: str,
    numero_edicao: int,
    service: EdicaoService = Depends(get_edicao_service),
):
    try:
        service.deletar(nome_jornal, numero_edicao)
    except EdicaoNaoEncontradaError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return RedirectResponse(url="/edicoes", status_code=303)
