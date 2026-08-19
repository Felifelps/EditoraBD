from datetime import date
from pydantic import BaseModel, ConfigDict


class MateriaBase(BaseModel):
    titulo: str
    subtitulo: str | None = None
    resumo: str | None = None
    conteudo: str
    data: date
    status: int
    nome_jornal: str | None = None
    numero_edicao: int | None = None
    id_setor: int | None = None


class MateriaCriar(MateriaBase):
    pass


class MateriaAtualizar(BaseModel):
    titulo: str | None = None
    subtitulo: str | None = None
    resumo: str | None = None
    conteudo: str | None = None
    data: date | None = None
    status: int | None = None
    nome_jornal: str | None = None
    numero_edicao: int | None = None
    id_setor: int | None = None


class Materia(MateriaBase):
    id_materia: int

    model_config = ConfigDict(from_attributes=True)
