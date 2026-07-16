import bcrypt
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

from app.config import Settings


def hash_password(senha: str) -> str:
    return bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()


def verify_password(senha: str, senha_hash: str) -> bool:
    return bcrypt.checkpw(senha.encode(), senha_hash.encode())


def create_session_token(cpf: str, settings: Settings) -> str:
    serializer = URLSafeTimedSerializer(settings.secret_key, salt="session")
    return serializer.dumps({"cpf": cpf})


def read_session_token(token: str, settings: Settings) -> str | None:
    serializer = URLSafeTimedSerializer(settings.secret_key, salt="session")
    try:
        data = serializer.loads(token, max_age=settings.session_max_age)
    except (BadSignature, SignatureExpired):
        return None
    return data.get("cpf")
