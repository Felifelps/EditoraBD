from fastapi import Depends, Request
from psycopg import Connection

from app.db.dependencies import get_conn
from app.exceptions.auth import CredenciaisInvalidasError, NaoAutenticadoError
from app.repositories.auth import AuthRepository
from app.security import verificar_senha


class AuthService:
    def __init__(self, repo: AuthRepository):
        self.repo = repo

    def autenticar(self, email: str, senha: str) -> dict:
        funcionario = self.repo.buscar_por_email(email)
        if funcionario is None or not funcionario["senha_hash"]:
            raise CredenciaisInvalidasError("E-mail ou senha inválidos")
        if not verificar_senha(senha, funcionario["senha_hash"]):
            raise CredenciaisInvalidasError("E-mail ou senha inválidos")
        return funcionario


def get_auth_service(conn: Connection = Depends(get_conn)) -> AuthService:
    return AuthService(AuthRepository(conn))


def obter_usuario_logado(request: Request) -> dict:
    """Dependency de protecao de rota: exige sessao autenticada."""
    cpf = request.session.get("cpf")
    if not cpf:
        raise NaoAutenticadoError()
    return {"cpf": cpf, "nome": request.session.get("nome")}
