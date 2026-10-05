import bcrypt

LIMITE_BYTES_BCRYPT = 72

def _codificar(senha: str) -> bytes:
    return senha.encode("utf-8")[:LIMITE_BYTES_BCRYPT]

def gerar_hash_senha(senha: str) -> str:
    return bcrypt.hashpw(_codificar(senha), bcrypt.gensalt()).decode("utf-8")

def verificar_senha(senha: str, senha_hash: str) -> bool:
    try:
        return bcrypt.checkpw(_codificar(senha), senha_hash.encode("utf-8"))
    except ValueError:
        return False