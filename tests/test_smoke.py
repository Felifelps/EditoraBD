"""
Testes de integracao ponta a ponta (frontend -> backend -> banco).

Rodam contra um Postgres real (nao usam mocks, seguindo o padrao do projeto).
Pre-requisito: `docker compose up -d db` (ou a stack completa) rodando, com o
banco acessivel em DATABASE_URL (por padrao localhost:5432, ver app/config.py).

Executar com: uv run pytest
"""

from fastapi.testclient import TestClient

from app.main import app

EMAIL_TESTE = "teste@editorabd.com"
SENHA_TESTE = "senha123"


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


def test_views_estao_criadas_e_relatorios_exibe_todas():
    with TestClient(app) as client:
        _logar(client)
        resp = client.get("/relatorios")
        assert resp.status_code == 200
        for titulo in (
            "Resumo de edições por jornal",
            "Carga de matérias por jornalista",
            "Setores e editores-chefes",
            "Detalhes dos funcionários",
            "Catálogo completo de matérias",
        ):
            assert titulo in resp.text
        assert "alert-danger" not in resp.text
        assert "relatorios-grid" in resp.text
        assert "relatorio-scroll" in resp.text


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
