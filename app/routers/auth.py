from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from psycopg import Connection

from app.auth.security import create_session_token, verify_password
from app.config import Settings, get_settings
from app.db.dependencies import get_conn
from app.repositories import funcionarios
from app.templating import templates

router = APIRouter()


@router.get("/login")
def login_form(request: Request):
    return templates.TemplateResponse(request, "auth/login.html", {"erro": None})


@router.post("/login")
def login_submit(
    request: Request,
    email: str = Form(...),
    senha: str = Form(...),
    conn: Connection = Depends(get_conn),
    settings: Settings = Depends(get_settings),
):
    usuario = funcionarios.buscar_por_email(conn, email)
    if usuario is None or not verify_password(senha, usuario.senha_hash):
        return templates.TemplateResponse(
            request, "auth/login.html", {"erro": "Email ou senha invalidos"}, status_code=401
        )

    token = create_session_token(usuario.cpf, settings)
    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(
        key=settings.session_cookie_name,
        value=token,
        httponly=True,
        max_age=settings.session_max_age,
    )
    return response


@router.post("/logout")
def logout(settings: Settings = Depends(get_settings)):
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie(settings.session_cookie_name)
    return response
