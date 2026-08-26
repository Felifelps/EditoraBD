import csv
import io
import logging

from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse
from psycopg import Connection

from app.db.dependencies import get_conn
from app.repositories.relatorios import RelatorioRepository
from app.services.auth import obter_usuario_logado
from app.templating import templates


router = APIRouter(prefix="/relatorios", dependencies=[Depends(obter_usuario_logado)])
logger = logging.getLogger(__name__)


def _consultar(repo: RelatorioRepository, consulta):
    try:
        return consulta(), None
    except Exception:
        logger.exception("Falha ao consultar relatorio")
        repo.conn.rollback()
        return [], "Nao foi possivel carregar este relatorio. Tente novamente."


TOP_N_RANKING = 10


def _grafico_resumo_edicoes(linhas: list[dict]) -> dict:
    ordenado = sorted(
        linhas,
        key=lambda linha: linha["total_edicoes"] or 0,
        reverse=True,
    )[:TOP_N_RANKING]

    return {
        "labels": [linha["nome_jornal"] for linha in ordenado],
        "totais": [int(linha["total_edicoes"] or 0) for linha in ordenado],
        "editores": [
            linha["nome_diretor"] or "Sem diretor"
            for linha in ordenado
        ],
        "ultimas": [
            linha["ultima_edicao"].strftime("%d/%m/%Y")
            if linha["ultima_edicao"]
            else "-"
            for linha in ordenado
        ],
    }


def _grafico_carga_jornalista(linhas: list[dict]) -> dict:
    ordenado = sorted(
        linhas,
        key=lambda linha: linha["total_materias"] or 0,
        reverse=True,
    )[:TOP_N_RANKING]

    return {
        "labels": [linha["nome_jornalista"] for linha in ordenado],
        "aprovadas": [
            int(linha["materias_aprovadas"] or 0)
            for linha in ordenado
        ],
        "em_andamento": [
            int(linha["materias_em_andamento"] or 0)
            for linha in ordenado
        ],
        "reprovadas": [
            int(linha["materias_reprovadas"] or 0)
            for linha in ordenado
        ],
    }


def _grafico_especialidades(linhas: list[dict]) -> dict:
    contagem: dict[str, int] = {}

    for linha in linhas:
        for especialidade in (linha["especialidades"] or "").split(","):
            especialidade = especialidade.strip()

            if especialidade:
                contagem[especialidade] = (
                    contagem.get(especialidade, 0) + 1
                )

    ordenado = sorted(
        contagem.items(),
        key=lambda item: item[1],
        reverse=True,
    )

    return {
        "labels": [nome for nome, _ in ordenado],
        "totais": [total for _, total in ordenado],
    }


def _grafico_cargos(linhas: list[dict]) -> dict:
    contagem: dict[str, int] = {}

    for linha in linhas:
        cargo = linha["cargo"] or "Sem cargo"
        contagem[cargo] = contagem.get(cargo, 0) + 1

    return {
        "labels": list(contagem.keys()),
        "totais": list(contagem.values()),
    }


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

    dados_resumo, erro_resumo = relatorios["resumo_edicoes_jornal"]
    dados_carga, erro_carga = relatorios["carga_materias_jornalista"]
    dados_setores, erro_setores = relatorios["setores_editores"]
    dados_funcionarios, erro_funcionarios = relatorios["funcionarios_detalhes"]
    dados_materias, erro_materias = relatorios["materias_completas"]

    graficos = {
        "resumo_edicoes_jornal": (
            None
            if erro_resumo
            else _grafico_resumo_edicoes(dados_resumo)
        ),
        "carga_materias_jornalista": (
            None
            if erro_carga
            else _grafico_carga_jornalista(dados_carga)
        ),
        "setores_editores": (
            None
            if erro_setores
            else _grafico_especialidades(dados_setores)
        ),
        "funcionarios_detalhes": (
            None
            if erro_funcionarios
            else _grafico_cargos(dados_funcionarios)
        ),
    }

    indicadores = {
        "jornais": len(dados_resumo) if not erro_resumo else None,
        "edicoes": (
            sum(l["total_edicoes"] or 0 for l in dados_resumo)
            if not erro_resumo
            else None
        ),
        "jornalistas": len(dados_carga) if not erro_carga else None,
        "materias": len(dados_materias) if not erro_materias else None,
    }

    return templates.TemplateResponse(
        request,
        "relatorios/list.html",
        {
            "relatorios": relatorios,
            "graficos": graficos,
            "indicadores": indicadores,
        },
    )

RELATORIOS_CSV = {
    "resumo_edicoes_jornal": (
        "resumo_edicoes_jornal",
        [
            "nome_jornal",
            "nome_diretor",
            "total_edicoes",
            "ultima_edicao",
        ],
    ),
    "carga_materias_jornalista": (
        "carga_materias_jornalista",
        [
            "cpf_jornalista",
            "nome_jornalista",
            "mtb",
            "total_materias",
            "materias_aprovadas",
            "materias_reprovadas",
            "materias_em_andamento",
        ],
    ),
    "setores_editores": (
        "setores_editores",
        [
            "id_setor",
            "nome_setor",
            "descricao_setor",
            "cpf_editor_chefe",
            "nome_editor",
            "especialidades",
        ],
    ),
    "funcionarios_detalhes": (
        "funcionarios_detalhes",
        [
            "cpf",
            "nome",
            "email",
            "telefone",
            "salario",
            "data_inicio_mandato",
            "mtb",
            "cargo",
        ],
    ),
    "materias_completas": (
        "materias_completas",
        [
            "id_materia",
            "titulo",
            "data_materia",
            "status_texto",
            "nome_setor",
            "numero_edicao",
            "nome_jornal",
            "autores",
        ],
    ),
}


@router.get("/{nome_relatorio}/csv")
def exportar_csv(
    nome_relatorio: str,
    conn: Connection = Depends(get_conn),
):
    if nome_relatorio not in RELATORIOS_CSV:
        return StreamingResponse(
            io.StringIO("Relatorio nao encontrado"),
            media_type="text/plain",
            status_code=404,
        )

    nome_consulta, colunas = RELATORIOS_CSV[nome_relatorio]

    repo = RelatorioRepository(conn)

    consultas = {
        "resumo_edicoes_jornal": repo.resumo_edicoes_jornal,
        "carga_materias_jornalista": repo.carga_materias_jornalista,
        "setores_editores": repo.setores_editores,
        "funcionarios_detalhes": repo.funcionarios_detalhes,
        "materias_completas": repo.materias_completas,
    }

    dados = consultas[nome_consulta]()

    arquivo = io.StringIO()
    escritor = csv.writer(arquivo)

    escritor.writerow(colunas)

    for linha in dados:
        valores = []

        for coluna in colunas:
            valor = linha.get(coluna)

            if valor is None:
                valor = ""
            elif hasattr(valor, "isoformat"):
                valor = valor.isoformat()

            valores.append(valor)

        escritor.writerow(valores)

    arquivo.seek(0)

    return StreamingResponse(
        iter([arquivo.getvalue()]),
        media_type="text/csv; charset=utf-8",
        headers={
            "Content-Disposition": (
                f'attachment; filename="{nome_relatorio}.csv"'
            )
        },
    )