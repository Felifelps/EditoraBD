from fastapi import Depends, HTTPException, Request
from psycopg import Connection

from app.auth.security import read_session_token
from app.config import Settings, get_settings
from app.db.dependencies import get_conn
from app.repositories import funcionarios
from app.schemas.funcionario import UsuarioSessao


def get_current_user(
    request: Request,
    conn: Connection = Depends(get_conn),
    settings: Settings = Depends(get_settings),
) -> UsuarioSessao | None:
    token = request.cookies.get(settings.session_cookie_name)
    if not token:
        return None
    cpf = read_session_token(token, settings)
    if not cpf:
        return None
    return funcionarios.buscar_por_cpf(conn, cpf)


def require_login(user: UsuarioSessao | None = Depends(get_current_user)) -> UsuarioSessao:
    if user is None:
        raise HTTPException(status_code=303, headers={"Location": "/login"})
    return user


def require_role(*papeis: str):
    def dependency(user: UsuarioSessao = Depends(require_login)) -> UsuarioSessao:
        if user.tipo not in papeis:
            raise HTTPException(status_code=403, detail="Acesso negado para este papel")
        return user

    return dependency
