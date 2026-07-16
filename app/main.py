from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import Depends, FastAPI, Request
from fastapi.staticfiles import StaticFiles

from app.auth.dependencies import require_login
from app.config import get_settings
from app.db.migrate import run_migrations
from app.db.pool import build_pool
from app.routers import auth
from app.schemas.funcionario import UsuarioSessao
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


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory=Path(__file__).resolve().parent / "static"), name="static")
app.include_router(auth.router)


@app.get("/")
def home(request: Request, user: UsuarioSessao = Depends(require_login)):
    return templates.TemplateResponse(request, "home.html", {"user": user})
