from pydantic import BaseModel


class JornalBase(BaseModel):
    cpf_diretor: str | None = None


class JornalCreate(JornalBase):
    nome_jornal: str


class JornalUpdate(JornalBase):
    pass


class Jornal(JornalBase):
    nome_jornal: str
    nome_diretor: str | None = None
