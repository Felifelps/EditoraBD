from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from app.config import get_settings
from app.db.migrate import run_migrations
from app.db.pool import build_pool
from app.routers import (
    edicoes,
    funcionarios,
    jornais,
    materias,
    relatorios,
    setores,
)
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

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static",
)

app.include_router(funcionarios.router)
app.include_router(materias.router)
app.include_router(jornais.router)
app.include_router(edicoes.router)
app.include_router(setores.router)
app.include_router(relatorios.router)


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request,
        "home.html",
        {},
    )