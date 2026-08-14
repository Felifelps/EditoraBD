from datetime import date
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel

Tipo = Literal["diretor", "jornalista", "editor_chefe"]


class FuncionarioBase(BaseModel):
    nome: str
    rua: str | None = None
    cep: str | None = None
    numero: str | None = None
    data_nascimento: date
    email: str
    telefone: str | None = None
    salario: Decimal


class FuncionarioCreate(FuncionarioBase):
    cpf: str
    tipo: Tipo


class FuncionarioUpdate(FuncionarioBase):
    tipo: Tipo


class Funcionario(FuncionarioBase):
    cpf: str
    tipo: Tipo | None = None
