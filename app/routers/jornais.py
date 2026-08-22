from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse

from app.exceptions.jornais import JornalJaExisteError, JornalNaoEncontradoError
from app.schemas.jornal import JornalCreate, JornalUpdate
from app.services.jornais import JornalService, get_jornal_service
from app.templating import templates

router = APIRouter(prefix="/jornais")


@router.get("")
def listar(request: Request, service: JornalService = Depends(get_jornal_service)):
    return templates.TemplateResponse(request, "jornais/list.html", {"jornais": service.listar()})


@router.get("/novo")
def form_novo(request: Request, service: JornalService = Depends(get_jornal_service)):
    return templates.TemplateResponse(
        request,
        "jornais/form.html",
        {"erro": None, "jornal": None, "acao": "/jornais/novo", "diretores": service.listar_diretores()},
    )


@router.post("/novo")
def criar(
    request: Request,
    nome_jornal: str = Form(...),
    cpf_diretor: str = Form(""),
    service: JornalService = Depends(get_jornal_service),
):
    dados = JornalCreate(nome_jornal=nome_jornal, cpf_diretor=cpf_diretor or None)
    try:
        service.criar(dados)
    except JornalJaExisteError as exc:
        return templates.TemplateResponse(
            request,
            "jornais/form.html",
            {
                "erro": str(exc),
                "jornal": None,
                "acao": "/jornais/novo",
                "diretores": service.listar_diretores(),
            },
            status_code=409,
        )
    return RedirectResponse(url="/jornais", status_code=303)


@router.get("/{nome_jornal}")
def detalhar(request: Request, nome_jornal: str, service: JornalService = Depends(get_jornal_service)):
    jornal = service.buscar(nome_jornal)
    if jornal is None:
        raise HTTPException(status_code=404, detail="Jornal nao encontrado")
    return templates.TemplateResponse(request, "jornais/detail.html", {"jornal": jornal})


@router.get("/{nome_jornal}/editar")
def form_editar(request: Request, nome_jornal: str, service: JornalService = Depends(get_jornal_service)):
    jornal = service.buscar(nome_jornal)
    if jornal is None:
        raise HTTPException(status_code=404, detail="Jornal nao encontrado")
    return templates.TemplateResponse(
        request,
        "jornais/form.html",
        {
            "erro": None,
            "jornal": jornal,
            "acao": f"/jornais/{nome_jornal}/editar",
            "diretores": service.listar_diretores(),
        },
    )


@router.post("/{nome_jornal}/editar")
def atualizar(
    request: Request,
    nome_jornal: str,
    cpf_diretor: str = Form(""),
    service: JornalService = Depends(get_jornal_service),
):
    dados = JornalUpdate(cpf_diretor=cpf_diretor or None)
    try:
        service.atualizar(nome_jornal, dados)
    except JornalNaoEncontradoError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return RedirectResponse(url=f"/jornais/{nome_jornal}", status_code=303)


@router.post("/{nome_jornal}/deletar")
def deletar(nome_jornal: str, service: JornalService = Depends(get_jornal_service)):
    try:
        service.deletar(nome_jornal)
    except JornalNaoEncontradoError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return RedirectResponse(url="/jornais", status_code=303)
