# Imagem oficial leve do Python (pyproject.toml exige requires-python >= 3.12)
FROM python:3.12-slim

# Copia o binário do uv diretamente da imagem oficial (multistage build)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Evita que o Python escreva arquivos .pyc no disco
ENV PYTHONDONTWRITEBYTECODE=1

# Garante que as saídas dos logs apareçam imediatamente no console
ENV PYTHONUNBUFFERED=1

# Instala as dependências do sistema necessárias
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Se você usa pyproject.toml / uv.lock (Recomendado pelo uv):
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache

# --- OU SE VOCÊ AINDA USA REQUIREMENTS.TXT, USE ESTAS DUAS LINHAS ABAIXO: ---
# COPY requirements.txt .
# RUN uv pip install --no-cache -r requirements.txt --system

# Copia o restante do código do projeto
COPY . .

# Expõe a porta que o FastAPI vai rodar
EXPOSE 8000

# Executa a aplicação usando o uv para rodar o ambiente virtual sincronizado
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
