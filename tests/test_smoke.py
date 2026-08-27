"""
Testes de integracao ponta a ponta (frontend -> backend -> banco).

Rodam contra um Postgres real (nao usam mocks, seguindo o padrao do projeto).
Pre-requisito: `docker compose up -d db` (ou a stack completa) rodando, com o
banco acessivel em DATABASE_URL (por padrao localhost:5432, ver app/config.py).

Executar com: uv run pytest
"""

import json
import re

from fastapi.testclient import TestClient

from app.main import app
from app.repositories.relatorios import RelatorioRepository

EMAIL_TESTE = "teste@editorabd.com"
SENHA_TESTE = "senha123"


def _grafico_do_html(html: str, variavel: str) -> dict:
    match = re.search(rf"var {variavel}\s*=\s*(\{{.*?\}});", html, re.S)
    assert match, f"variavel {variavel} nao encontrada no HTML"
    return json.loads(match.group(1))


def _logar(client: TestClient) -> None:
    resp = client.post("/login", data={"email": EMAIL_TESTE, "senha": SENHA_TESTE})
    assert resp.status_code in (200, 303)


def test_paginas_principais_exigem_login():
    with TestClient(app, follow_redirects=False) as client:
        for path in ("/", "/funcionarios", "/jornais", "/edicoes", "/setores", "/materias", "/relatorios"):
            resp = client.get(path)
            assert resp.status_code == 303, f"{path} -> {resp.status_code}"
            assert resp.headers["location"] == "/login"


def test_login_com_credenciais_invalidas():
    with TestClient(app) as client:
        resp = client.post("/login", data={"email": EMAIL_TESTE, "senha": "senha-errada"})
        assert resp.status_code == 401
        assert "inválid" in resp.text.lower()


def test_login_com_credenciais_validas_e_acesso_as_paginas():
    with TestClient(app, follow_redirects=False) as client:
        resp = client.post("/login", data={"email": EMAIL_TESTE, "senha": SENHA_TESTE})
        assert resp.status_code == 303
        assert resp.headers["location"] == "/relatorios"

        for path in ("/", "/funcionarios", "/jornais", "/edicoes", "/setores", "/materias", "/relatorios"):
            resp = client.get(path)
            if path == "/":
                assert resp.status_code == 303
                assert resp.headers["location"] == "/relatorios"
            else:
                assert resp.status_code == 200, f"{path} -> {resp.status_code}"


def test_logout_revoga_acesso():
    with TestClient(app, follow_redirects=False) as client:
        _logar(client)
        assert client.get("/relatorios").status_code == 200

        resp = client.post("/logout")
        assert resp.status_code == 303
        assert resp.headers["location"] == "/login"

        resp = client.get("/relatorios")
        assert resp.status_code == 303
        assert resp.headers["location"] == "/login"


def test_dashboard_de_relatorios_exibe_as_6_views():
    with TestClient(app) as client:
        _logar(client)
        resp = client.get("/relatorios")
        assert resp.status_code == 200

        # as 6 views representadas, todas com grafico + tabela
        for canvas_id in (
            "graficoResumoEdicoes",
            "graficoCargaJornalista",
            "graficoEspecialidades",
            "graficoCargos",
            "graficoStatusMaterias",
            "graficoHistoricoStatus",
        ):
            assert f'id="{canvas_id}"' in resp.text
        assert "Catálogo completo de matérias" in resp.text
        assert "Histórico de status de matéria" in resp.text

        # indicadores (KPIs) calculados a partir dos dados das views
        assert "kpi-grid" in resp.text
        assert "kpi-valor" in resp.text

        # layout em dashboard: grid responsivo + scroll interno por card
        assert "relatorios-grid" in resp.text
        assert "chart-container" in resp.text
        assert "relatorio-scroll" in resp.text

        assert "chart.js" in resp.text
        assert "relatorio-estado-erro" not in resp.text


def test_crud_funcionario():
    cpf = "88877766655"
    with TestClient(app) as client:
        _logar(client)

        criar = client.post(
            "/funcionarios/novo",
            data={
                "cpf": cpf,
                "nome": "Funcionario Teste Pytest",
                "data_nascimento": "1990-01-01",
                "email": "pytest.funcionario@example.com",
                "salario": "3000",
                "tipo": "jornalista",
            },
        )
        assert criar.status_code in (200, 303)

        detalhe = client.get(f"/funcionarios/{cpf}")
        assert detalhe.status_code == 200
        assert "Funcionario Teste Pytest" in detalhe.text

        editar = client.post(
            f"/funcionarios/{cpf}/editar",
            data={
                "nome": "Funcionario Editado Pytest",
                "data_nascimento": "1990-01-01",
                "email": "pytest.funcionario@example.com",
                "salario": "3500",
                "tipo": "jornalista",
            },
        )
        assert editar.status_code in (200, 303)

        detalhe2 = client.get(f"/funcionarios/{cpf}")
        assert "Funcionario Editado Pytest" in detalhe2.text

        deletar = client.post(f"/funcionarios/{cpf}/deletar")
        assert deletar.status_code in (200, 303)

        detalhe3 = client.get(f"/funcionarios/{cpf}")
        assert detalhe3.status_code == 404


def test_atualizar_status_materia():
    with TestClient(app, follow_redirects=False) as client:
        _logar(client)

        detalhe = client.get("/materias/1")
        assert detalhe.status_code == 200
        assert "Aprovar" in detalhe.text
        assert "Reprovar" in detalhe.text
        assert "Em Andamento" in detalhe.text

        aprovar = client.post("/materias/1/status", data={"status": 1})
        assert aprovar.status_code == 303
        assert aprovar.headers["location"] == "/materias/1"

        detalhe_aprovada = client.get("/materias/1")
        assert "status-aprovada" in detalhe_aprovada.text

        reprovar = client.post("/materias/1/status", data={"status": 0})
        assert reprovar.status_code == 303

        detalhe_reprovada = client.get("/materias/1")
        assert "status-reprovada" in detalhe_reprovada.text

        em_andamento = client.post("/materias/1/status", data={"status": 2})
        assert em_andamento.status_code == 303

        detalhe_em_andamento = client.get("/materias/1")
        assert "status-em-andamento" in detalhe_em_andamento.text


def test_atualizar_status_materia_valor_invalido():
    with TestClient(app) as client:
        _logar(client)
        resp = client.post("/materias/1/status", data={"status": 9})
        assert resp.status_code == 400


def test_atualizar_status_materia_inexistente_retorna_404():
    with TestClient(app) as client:
        _logar(client)
        resp = client.post("/materias/999999/status", data={"status": 1})
        assert resp.status_code == 404


def test_fk_invalida_retorna_erro_tratado_nao_500():
    with TestClient(app, raise_server_exceptions=False) as client:
        _logar(client)
        resp = client.post(
            "/setores/novo",
            data={
                "id_setor": "9001",
                "nome": "Setor Teste FK Invalida",
                "descricao": "teste",
                "cpf_editor_chefe": "00000000000",
            },
        )
        assert resp.status_code == 400
        assert "Referência inválida" in resp.text


def test_dados_dos_graficos_correspondem_as_views():
    with TestClient(app) as client:
        _logar(client)
        resp = client.get("/relatorios")
        assert resp.status_code == 200
        html = resp.text

        # a mesma app/pool ja esta de pe (lifespan ativo dentro do `with`) — consulta
        # as views diretamente para comparar com o que foi embutido no HTML
        with app.state.pool.connection() as conn:
            repo = RelatorioRepository(conn)

            # os graficos de ranking mostram so o Top 10 (para caber legivel no
            # espaco), mas a tabela ao lado continua com todas as linhas da View
            TOP_N = 10

            resumo = repo.resumo_edicoes_jornal()
            top_resumo = sorted(resumo, key=lambda l: l["total_edicoes"] or 0, reverse=True)[:TOP_N]
            grafico_resumo = _grafico_do_html(html, "graficoResumoEdicoes")
            assert sorted(grafico_resumo["totais"], reverse=True) == grafico_resumo["totais"]
            assert len(grafico_resumo["labels"]) == min(TOP_N, len(resumo))
            assert sum(grafico_resumo["totais"]) == sum(l["total_edicoes"] or 0 for l in top_resumo)
            assert set(grafico_resumo["labels"]) == {l["nome_jornal"] for l in top_resumo}
            # a tabela complementar continua com a lista completa, nao so o Top 10
            assert all(l["nome_jornal"] in html for l in resumo)

            carga = repo.carga_materias_jornalista()
            top_carga = sorted(carga, key=lambda l: l["total_materias"] or 0, reverse=True)[:TOP_N]
            grafico_carga = _grafico_do_html(html, "graficoCargaJornalista")
            assert len(grafico_carga["labels"]) == min(TOP_N, len(carga))
            assert set(grafico_carga["labels"]) == {l["nome_jornalista"] for l in top_carga}
            assert sum(grafico_carga["aprovadas"]) == sum(l["materias_aprovadas"] or 0 for l in top_carga)
            assert sum(grafico_carga["reprovadas"]) == sum(l["materias_reprovadas"] or 0 for l in top_carga)
            assert sum(grafico_carga["em_andamento"]) == sum(l["materias_em_andamento"] or 0 for l in top_carga)

            cargos = repo.funcionarios_detalhes()
            grafico_cargos = _grafico_do_html(html, "graficoCargos")
            assert sum(grafico_cargos["totais"]) == len(cargos)


def test_crud_pages_seguem_o_mesmo_padrao_visual():
    """As 5 entidades usam o mesmo cabecalho de pagina e cartao de formulario."""
    with TestClient(app) as client:
        _logar(client)

        paginas_lista = ["/funcionarios", "/jornais", "/edicoes", "/setores", "/materias"]
        for path in paginas_lista:
            resp = client.get(path)
            assert resp.status_code == 200
            assert "page-header" in resp.text, path
            assert 'class="card shadow-sm border-0' in resp.text, path

        paginas_form = ["/funcionarios/novo", "/jornais/novo", "/edicoes/novo", "/setores/novo", "/materias/novo"]
        for path in paginas_form:
            resp = client.get(path)
            assert resp.status_code == 200
            assert "page-header" in resp.text, path
            assert "form-card-wrap" in resp.text, path
            assert "form-card" in resp.text, path
            assert "btn-outline-secondary" in resp.text, path  # botao Cancelar

        # detalhe de um registro existente por entidade tambem usa o mesmo card
        detalhes = [
            "/funcionarios/10000000001",
            "/jornais/Jornal Pernambuco".replace(" ", "%20"),
            "/setores/1",
            "/materias/1",
        ]
        for path in detalhes:
            resp = client.get(path)
            assert resp.status_code == 200
            assert "detail-card" in resp.text, path
            assert "detail-grid" in resp.text, path
