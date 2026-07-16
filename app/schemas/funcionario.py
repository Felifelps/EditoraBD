from pydantic import BaseModel


class FuncionarioAuth(BaseModel):
    cpf: str
    nome: str
    email: str
    senha_hash: str
    tipo: str


class UsuarioSessao(BaseModel):
    cpf: str
    nome: str
    email: str
    tipo: str
