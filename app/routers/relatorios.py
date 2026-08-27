import logging

from datetime import date, datetime
from decimal import Decimal

from fastapi import APIRouter, Depends, Request, Response, HTTPException
from psycopg import Connection
from fpdf import FPDF

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
    ordenado = sorted(linhas, key=lambda linha: linha["total_edicoes"] or 0, reverse=True)[:TOP_N_RANKING]
    return {
        "labels": [linha["nome_jornal"] for linha in ordenado],
        "totais": [int(linha["total_edicoes"] or 0) for linha in ordenado],
        "editores": [linha["nome_diretor"] or "Sem diretor" for linha in ordenado],
        "ultimas": [
            linha["ultima_edicao"].strftime("%d/%m/%Y") if linha["ultima_edicao"] else "-"
            for linha in ordenado
        ],
    }


def _grafico_carga_jornalista(linhas: list[dict]) -> dict:
    ordenado = sorted(linhas, key=lambda linha: linha["total_materias"] or 0, reverse=True)[:TOP_N_RANKING]
    return {
        "labels": [linha["nome_jornalista"] for linha in ordenado],
        "aprovadas": [int(linha["materias_aprovadas"] or 0) for linha in ordenado],
        "em_andamento": [int(linha["materias_em_andamento"] or 0) for linha in ordenado],
        "reprovadas": [int(linha["materias_reprovadas"] or 0) for linha in ordenado],
    }


def _grafico_especialidades(linhas: list[dict]) -> dict:
    contagem: dict[str, int] = {}
    for linha in linhas:
        for especialidade in (linha["especialidades"] or "").split(","):
            especialidade = especialidade.strip()
            if especialidade:
                contagem[especialidade] = contagem.get(especialidade, 0) + 1
    ordenado = sorted(contagem.items(), key=lambda item: item[1], reverse=True)
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


def _grafico_status_materias(linhas: list[dict]) -> dict:
    contagem: dict[str, int] = {}
    for linha in linhas:
        status = linha["status_texto"] or "Sem status"
        contagem[status] = contagem.get(status, 0) + 1
    return {
        "labels": list(contagem.keys()),
        "totais": list(contagem.values()),
    }


def _grafico_historico_status_materia(linhas: list[dict]) -> dict:
    contagem: dict[str, int] = {}
    for linha in linhas:
        status_novo = linha["status_novo_texto"] or "Sem status"
        contagem[status_novo] = contagem.get(status_novo, 0) + 1
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
        "historico_status_materia": repo.historico_status_materia,
    }
    relatorios = {}
    for nome, consulta in consultas.items():
        relatorios[nome] = _consultar(repo, consulta)

    dados_resumo, erro_resumo = relatorios["resumo_edicoes_jornal"]
    dados_carga, erro_carga = relatorios["carga_materias_jornalista"]
    dados_setores, erro_setores = relatorios["setores_editores"]
    dados_funcionarios, erro_funcionarios = relatorios["funcionarios_detalhes"]
    dados_materias, erro_materias = relatorios["materias_completas"]
    dados_historico, erro_historico = relatorios["historico_status_materia"]

    graficos = {
        "resumo_edicoes_jornal": None if erro_resumo else _grafico_resumo_edicoes(dados_resumo),
        "carga_materias_jornalista": None if erro_carga else _grafico_carga_jornalista(dados_carga),
        "setores_editores": None if erro_setores else _grafico_especialidades(dados_setores),
        "funcionarios_detalhes": None if erro_funcionarios else _grafico_cargos(dados_funcionarios),
        "materias_completas": None if erro_materias else _grafico_status_materias(dados_materias),
        "historico_status_materia": None if erro_historico else _grafico_historico_status_materia(dados_historico),
    }

    indicadores = {
        "jornais": len(dados_resumo) if not erro_resumo else None,
        "edicoes": sum(l["total_edicoes"] or 0 for l in dados_resumo) if not erro_resumo else None,
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

def _gerar_pdf(nome: str, dados: list[dict]) -> bytes:
    pdf = FPDF()
    pdf.add_page(orientation="L")
    pdf.set_font("helvetica", size=10)
    
    pdf.set_font("helvetica", style="B", size=14)
    pdf.cell(0, 10, f"Relatorio: {nome.replace('_', ' ').title()}", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(5)
    
    if not dados:
        pdf.set_font("helvetica", size=10)
        pdf.cell(0, 10, "Nenhum dado encontrado.", new_x="LMARGIN", new_y="NEXT")
        return pdf.output()
        
    colunas = list(dados[0].keys())
    col_width = pdf.epw / len(colunas)
    line_height = 8
    
    pdf.set_font("helvetica", style="B", size=9)
    for col in colunas:
        pdf.cell(col_width, line_height, col.replace('_', ' ').title(), border=1)
    pdf.ln(line_height)
    
    pdf.set_font("helvetica", size=8)
    for linha in dados:
        for col in colunas:
            val = linha.get(col)
            if val is None:
                txt = "-"
            elif isinstance(val, (date, datetime)):
                txt = val.strftime("%d/%m/%Y")
            elif isinstance(val, Decimal):
                txt = f"R$ {val:,.2f}"
            else:
                txt = str(val)
                
            if len(txt) > 35:
                txt = txt[:32] + "..."
            
            # Use latin-1 encoding to prevent character errors on basic fonts
            txt = txt.encode('latin-1', 'replace').decode('latin-1')
            pdf.cell(col_width, line_height, txt, border=1)
        pdf.ln(line_height)
        
    return pdf.output()

@router.get("/{nome}/pdf")
def exportar_pdf(nome: str, conn: Connection = Depends(get_conn)):
    repo = RelatorioRepository(conn)
    consultas = {
        "resumo_edicoes_jornal": repo.resumo_edicoes_jornal,
        "carga_materias_jornalista": repo.carga_materias_jornalista,
        "setores_editores": repo.setores_editores,
        "funcionarios_detalhes": repo.funcionarios_detalhes,
        "materias_completas": repo.materias_completas,
        "historico_status_materia": repo.historico_status_materia,
    }

    if nome not in consultas:
        raise HTTPException(status_code=404, detail="Relatorio nao encontrado")
        
    dados, erro = _consultar(repo, consultas[nome])
    if erro:
        raise HTTPException(status_code=500, detail=erro)
        
    pdf_bytes = _gerar_pdf(nome, dados)
    
    return Response(
        content=bytes(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{nome}.pdf"'}
    )
