import hashlib
import hmac
import secrets

_ALGORITMO = "sha256"
_ITERACOES = 260_000


def hash_senha(senha: str) -> str:
    """Gera um hash salgado (PBKDF2-HMAC-SHA256) no formato "salt$hash"."""
    salt = secrets.token_hex(16)
    hash_bytes = hashlib.pbkdf2_hmac(_ALGORITMO, senha.encode("utf-8"), bytes.fromhex(salt), _ITERACOES)
    return f"{salt}${hash_bytes.hex()}"


def verificar_senha(senha: str, senha_hash: str) -> bool:
    """Confere `senha` contra um hash gerado por `hash_senha`."""
    salt, _, hash_esperado = senha_hash.partition("$")
    if not salt or not hash_esperado:
        return False
    hash_calculado = hashlib.pbkdf2_hmac(_ALGORITMO, senha.encode("utf-8"), bytes.fromhex(salt), _ITERACOES).hex()
    return hmac.compare_digest(hash_calculado, hash_esperado)
