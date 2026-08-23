import logging

from fastapi import APIRouter, Depends, Request
from psycopg import Connection

from app.db.dependencies import get_conn
from app.repositories.relatorios import RelatorioRepository
from app.templating import templates


router = APIRouter(prefix="/relatorios")
logger = logging.getLogger(__name__)


def _consultar(repo: RelatorioRepository, consulta):
    try:
        return consulta(), None
    except Exception:
        logger.exception("Falha ao consultar relatorio")
        repo.conn.rollback()
        return [], "Nao foi possivel carregar este relatorio. Tente novamente."


@router.get("")
def listar(request: Request, conn: Connection = Depends(get_conn)):
    repo = RelatorioRepository(conn)
    consultas = {
        "resumo_edicoes_jornal": repo.resumo_edicoes_jornal,
        "carga_materias_jornalista": repo.carga_materias_jornalista,
        "setores_editores": repo.setores_editores,
        "funcionarios_detalhes": repo.funcionarios_detalhes,
        "materias_completas": repo.materias_completas,
    }
    relatorios = {}
    for nome, consulta in consultas.items():
        relatorios[nome] = _consultar(repo, consulta)

    return templates.TemplateResponse(request, "relatorios/list.html", {"relatorios": relatorios})