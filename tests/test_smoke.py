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
    match = re.search(rf"var {variavel} = (\{{.*?\}});", html, re.S)
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


def test_dashboard_de_relatorios_exibe_as_5_views():
    with TestClient(app) as client:
        _logar(client)
        resp = client.get("/relatorios")
        assert resp.status_code == 200

        # as 5 views continuam representadas: 4 em gráfico + tabela, 1 só em tabela
        for canvas_id in (
            "graficoResumoEdicoes",
            "graficoCargaJornalista",
            "graficoEspecialidades",
            "graficoCargos",
        ):
            assert f'id="{canvas_id}"' in resp.text
        assert "Catálogo completo de matérias" in resp.text

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

            resumo = repo.resumo_edicoes_jornal()
            grafico_resumo = _grafico_do_html(html, "graficoResumoEdicoes")
            assert sorted(grafico_resumo["totais"], reverse=True) == grafico_resumo["totais"]
            assert sum(grafico_resumo["totais"]) == sum(l["total_edicoes"] or 0 for l in resumo)
            assert set(grafico_resumo["labels"]) == {l["nome_jornal"] for l in resumo}

            carga = repo.carga_materias_jornalista()
            grafico_carga = _grafico_do_html(html, "graficoCargaJornalista")
            assert set(grafico_carga["labels"]) == {l["nome_jornalista"] for l in carga}
            assert sum(grafico_carga["aprovadas"]) == sum(l["materias_aprovadas"] or 0 for l in carga)
            assert sum(grafico_carga["reprovadas"]) == sum(l["materias_reprovadas"] or 0 for l in carga)
            assert sum(grafico_carga["em_andamento"]) == sum(l["materias_em_andamento"] or 0 for l in carga)

            cargos = repo.funcionarios_detalhes()
            grafico_cargos = _grafico_do_html(html, "graficoCargos")
            assert sum(grafico_cargos["totais"]) == len(cargos)
