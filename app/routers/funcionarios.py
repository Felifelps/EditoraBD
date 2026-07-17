from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse

from app.exceptions.funcionarios import FuncionarioJaExisteError, FuncionarioNaoEncontradoError
from app.schemas.funcionario import FuncionarioCreate, FuncionarioUpdate
from app.services.funcionarios import FuncionarioService, get_funcionario_service
from app.templating import templates

router = APIRouter(prefix="/funcionarios")


@router.get("")
def listar(request: Request, service: FuncionarioService = Depends(get_funcionario_service)):
    return templates.TemplateResponse(
        request, "funcionarios/list.html", {"funcionarios": service.listar()}
    )


@router.get("/novo")
def form_novo(request: Request):
    return templates.TemplateResponse(
        request,
        "funcionarios/form.html",
        {"erro": None, "funcionario": None, "acao": "/funcionarios/novo"},
    )


@router.post("/novo")
def criar(
    request: Request,
    cpf: str = Form(...),
    nome: str = Form(...),
    rua: str = Form(""),
    cep: str = Form(""),
    numero: str = Form(""),
    data_nascimento: str = Form(...),
    email: str = Form(...),
    telefone: str = Form(""),
    salario: str = Form(...),
    tipo: str = Form(...),
    service: FuncionarioService = Depends(get_funcionario_service),
):
    dados = FuncionarioCreate(
        cpf=cpf,
        nome=nome,
        rua=rua or None,
        cep=cep or None,
        numero=numero or None,
        data_nascimento=data_nascimento,
        email=email,
        telefone=telefone or None,
        salario=salario,
        tipo=tipo,
    )
    try:
        service.criar(dados)
    except FuncionarioJaExisteError as exc:
        return templates.TemplateResponse(
            request,
            "funcionarios/form.html",
            {"erro": str(exc), "funcionario": None, "acao": "/funcionarios/novo"},
            status_code=409,
        )
    return RedirectResponse(url="/funcionarios", status_code=303)


@router.get("/{cpf}")
def detalhar(request: Request, cpf: str, service: FuncionarioService = Depends(get_funcionario_service)):
    funcionario = service.buscar(cpf)
    if funcionario is None:
        raise HTTPException(status_code=404, detail="Funcionario nao encontrado")
    return templates.TemplateResponse(request, "funcionarios/detail.html", {"funcionario": funcionario})


@router.get("/{cpf}/editar")
def form_editar(request: Request, cpf: str, service: FuncionarioService = Depends(get_funcionario_service)):
    funcionario = service.buscar(cpf)
    if funcionario is None:
        raise HTTPException(status_code=404, detail="Funcionario nao encontrado")
    return templates.TemplateResponse(
        request,
        "funcionarios/form.html",
        {"erro": None, "funcionario": funcionario, "acao": f"/funcionarios/{cpf}/editar"},
    )


@router.post("/{cpf}/editar")
def atualizar(
    request: Request,
    cpf: str,
    nome: str = Form(...),
    rua: str = Form(""),
    cep: str = Form(""),
    numero: str = Form(""),
    data_nascimento: str = Form(...),
    email: str = Form(...),
    telefone: str = Form(""),
    salario: str = Form(...),
    tipo: str = Form(...),
    service: FuncionarioService = Depends(get_funcionario_service),
):
    dados = FuncionarioUpdate(
        nome=nome,
        rua=rua or None,
        cep=cep or None,
        numero=numero or None,
        data_nascimento=data_nascimento,
        email=email,
        telefone=telefone or None,
        salario=salario,
        tipo=tipo,
    )
    try:
        service.atualizar(cpf, dados)
    except FuncionarioNaoEncontradoError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return RedirectResponse(url=f"/funcionarios/{cpf}", status_code=303)


@router.post("/{cpf}/deletar")
def deletar(cpf: str, service: FuncionarioService = Depends(get_funcionario_service)):
    try:
        service.deletar(cpf)
    except FuncionarioNaoEncontradoError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return RedirectResponse(url="/funcionarios", status_code=303)
