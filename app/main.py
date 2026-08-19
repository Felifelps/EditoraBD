from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from app.config import get_settings
from app.db.migrate import run_migrations
from app.db.pool import build_pool
from app.routers import funcionarios, materias
from app.templating import templates


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    pool = build_pool(settings)

    pool.open(wait=True)

    run_migrations(pool)

    app.state.pool = pool

    yield

    pool.close()


app = FastAPI(
    lifespan=lifespan
)


app.mount(
    "/static",
    StaticFiles(
        directory=Path(__file__).resolve().parent / "static"
    ),
    name="static"
)


app.include_router(
    funcionarios.router
)

app.include_router(
    materias.router
)


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request,
        "home.html",
        {}
    )