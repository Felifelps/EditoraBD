from datetime import date
from decimal import Decimal

from pydantic import BaseModel


class FuncionarioBase(BaseModel):
    nome: str
    rua: str | None = None
    cep: str | None = None
    numero: str | None = None
    data_nascimento: date
    email: str
    telefone: str | None = None
    salario: Decimal
    tipo: str


class FuncionarioCreate(FuncionarioBase):
    cpf: str


class FuncionarioUpdate(FuncionarioBase):
    pass


class Funcionario(FuncionarioBase):
    cpf: str
