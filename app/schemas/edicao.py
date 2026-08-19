from datetime import date

from pydantic import BaseModel


class EdicaoBase(BaseModel):
    data: date | None = None


class EdicaoCreate(EdicaoBase):
    nome_jornal: str
    numero_edicao: int


class EdicaoUpdate(EdicaoBase):
    pass


class Edicao(EdicaoBase):
    nome_jornal: str
    numero_edicao: int
