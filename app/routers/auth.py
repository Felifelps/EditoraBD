from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse

from app.exceptions.auth import CredenciaisInvalidasError
from app.services.auth import AuthService, get_auth_service
from app.templating import templates

router = APIRouter()


@router.get("/login")
def form_login(request: Request):
    if request.session.get("cpf"):
        return RedirectResponse(url="/relatorios", status_code=303)
    return templates.TemplateResponse(request, "login.html", {"erro": None})


@router.post("/login")
def login(
    request: Request,
    email: str = Form(...),
    senha: str = Form(...),
    service: AuthService = Depends(get_auth_service),
):
    try:
        funcionario = service.autenticar(email, senha)
    except CredenciaisInvalidasError as exc:
        return templates.TemplateResponse(
            request,
            "login.html",
            {"erro": str(exc)},
            status_code=401,
        )

    request.session["cpf"] = funcionario["cpf"]
    request.session["nome"] = funcionario["nome"]
    return RedirectResponse(url="/relatorios", status_code=303)


@router.post("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)
