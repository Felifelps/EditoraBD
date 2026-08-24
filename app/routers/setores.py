from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse

from app.exceptions.setores import SetorJaExisteError, SetorNaoEncontradoError
from app.schemas.setor import SetorCreate, SetorUpdate
from app.services.auth import obter_usuario_logado
from app.services.setores import SetorService, get_setor_service
from app.templating import templates

router = APIRouter(prefix="/setores", dependencies=[Depends(obter_usuario_logado)])


@router.get("")
def listar(request: Request, service: SetorService = Depends(get_setor_service)):
    return templates.TemplateResponse(request, "setores/list.html", {"setores": service.listar()})


@router.get("/novo")
def form_novo(request: Request, service: SetorService = Depends(get_setor_service)):
    return templates.TemplateResponse(
        request,
        "setores/form.html",
        {"erro": None, "setor": None, "acao": "/setores/novo", "editores": service.listar_editores_chefe()},
    )


@router.post("/novo")
def criar(
    request: Request,
    id_setor: int = Form(...),
    nome: str = Form(...),
    descricao: str = Form(""),
    cpf_editor_chefe: str = Form(""),
    service: SetorService = Depends(get_setor_service),
):
    dados = SetorCreate(
        id_setor=id_setor,
        nome=nome,
        descricao=descricao or None,
        cpf_editor_chefe=cpf_editor_chefe or None,
    )
    try:
        service.criar(dados)
    except SetorJaExisteError as exc:
        return templates.TemplateResponse(
            request,
            "setores/form.html",
            {
                "erro": str(exc),
                "setor": None,
                "acao": "/setores/novo",
                "editores": service.listar_editores_chefe(),
            },
            status_code=409,
        )
    return RedirectResponse(url="/setores", status_code=303)


@router.get("/{id_setor}")
def detalhar(request: Request, id_setor: int, service: SetorService = Depends(get_setor_service)):
    setor = service.buscar(id_setor)
    if setor is None:
        raise HTTPException(status_code=404, detail="Setor nao encontrado")
    return templates.TemplateResponse(request, "setores/detail.html", {"setor": setor})


@router.get("/{id_setor}/editar")
def form_editar(request: Request, id_setor: int, service: SetorService = Depends(get_setor_service)):
    setor = service.buscar(id_setor)
    if setor is None:
        raise HTTPException(status_code=404, detail="Setor nao encontrado")
    return templates.TemplateResponse(
        request,
        "setores/form.html",
        {
            "erro": None,
            "setor": setor,
            "acao": f"/setores/{id_setor}/editar",
            "editores": service.listar_editores_chefe(),
        },
    )


@router.post("/{id_setor}/editar")
def atualizar(
    request: Request,
    id_setor: int,
    nome: str = Form(...),
    descricao: str = Form(""),
    cpf_editor_chefe: str = Form(""),
    service: SetorService = Depends(get_setor_service),
):
    dados = SetorUpdate(nome=nome, descricao=descricao or None, cpf_editor_chefe=cpf_editor_chefe or None)
    try:
        service.atualizar(id_setor, dados)
    except SetorNaoEncontradoError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return RedirectResponse(url=f"/setores/{id_setor}", status_code=303)


@router.post("/{id_setor}/deletar")
def deletar(id_setor: int, service: SetorService = Depends(get_setor_service)):
    try:
        service.deletar(id_setor)
    except SetorNaoEncontradoError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return RedirectResponse(url="/setores", status_code=303)
