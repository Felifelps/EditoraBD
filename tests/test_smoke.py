"""
Testes de integracao ponta a ponta (frontend -> backend -> banco).

Rodam contra um Postgres real (nao usam mocks, seguindo o padrao do projeto).
Pre-requisito: `docker compose up -d db` (ou a stack completa) rodando, com o
banco acessivel em DATABASE_URL (por padrao localhost:5432, ver app/config.py).

Executar com: uv run pytest
"""

from fastapi.testclient import TestClient

from app.main import app


def test_paginas_principais_carregam():
    with TestClient(app) as client:
        for path in ("/", "/funcionarios", "/jornais", "/edicoes", "/setores", "/materias", "/relatorios"):
            resp = client.get(path)
            assert resp.status_code == 200, f"{path} -> {resp.status_code}"


def test_views_estao_criadas_e_relatorios_exibe_todas():
    with TestClient(app) as client:
        resp = client.get("/relatorios")
        assert resp.status_code == 200
        for titulo in (
            "Resumo de edicoes por jornal",
            "Carga de materias por jornalista",
            "Setores e editores-chefes",
            "Detalhes dos funcionarios",
            "Catalogo completo de materias",
        ):
            assert titulo in resp.text
        assert "alert-danger" not in resp.text


def test_crud_funcionario():
    cpf = "88877766655"
    with TestClient(app) as client:
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
