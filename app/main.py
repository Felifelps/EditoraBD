from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from psycopg.errors import CheckViolation, ForeignKeyViolation
from starlette.middleware.sessions import SessionMiddleware

from app.config import get_settings
from app.db.migrate import run_migrations
from app.db.pool import build_pool
from app.exceptions.auth import NaoAutenticadoError
from app.routers import (
    auth,
    edicoes,
    funcionarios,
    jornais,
    materias,
    relatorios,
    setores,
)
from app.services.auth import obter_usuario_logado
from app.templating import templates


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    pool = build_pool(settings)

    pool.open()

    app.state.pool = pool

    run_migrations(pool)

    yield

    pool.close()


app = FastAPI(
    title="Gestao Editorial",
    lifespan=lifespan,
)

app.add_middleware(SessionMiddleware, secret_key=get_settings().session_secret)

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static",
)

app.include_router(auth.router)
app.include_router(funcionarios.router)
app.include_router(materias.router)
app.include_router(jornais.router)
app.include_router(edicoes.router)
app.include_router(setores.router)
app.include_router(relatorios.router)


@app.exception_handler(NaoAutenticadoError)
def nao_autenticado_handler(request: Request, exc: NaoAutenticadoError):
    return RedirectResponse(url="/login", status_code=303)


@app.exception_handler(ForeignKeyViolation)
def referencia_invalida_handler(request: Request, exc: ForeignKeyViolation):
    return templates.TemplateResponse(
        request,
        "erro.html",
        {"mensagem": "Referência inválida: o registro relacionado informado não existe."},
        status_code=400,
    )


@app.exception_handler(CheckViolation)
def valor_invalido_handler(request: Request, exc: CheckViolation):
    return templates.TemplateResponse(
        request,
        "erro.html",
        {"mensagem": "Valor inválido para um dos campos informados."},
        status_code=400,
    )


@app.get("/")
def home(request: Request, usuario: dict = Depends(obter_usuario_logado)):
    return RedirectResponse(url="/relatorios", status_code=303)


@app.get("/{caminho_invalido:path}", include_in_schema=False)
def rota_nao_encontrada(request: Request, caminho_invalido: str):
    """Qualquer URL sem rota correspondente cai aqui (registrada por ultimo, entao
    so pega o que nenhum router tratou): redireciona para /relatorios se houver
    sessao autenticada, senao para /login."""
    if request.session.get("cpf"):
        return RedirectResponse(url="/relatorios", status_code=303)
    return RedirectResponse(url="/login", status_code=303)