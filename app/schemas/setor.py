from pydantic import BaseModel


class SetorBase(BaseModel):
    nome: str
    descricao: str | None = None
    cpf_editor_chefe: str | None = None


class SetorCreate(SetorBase):
    id_setor: int


class SetorUpdate(SetorBase):
    pass


class Setor(SetorBase):
    id_setor: int
    nome_editor_chefe: str | None = None
