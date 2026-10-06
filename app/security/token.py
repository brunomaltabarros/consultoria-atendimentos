from datetime import datetime, timedelta, timezone

import jwt

from app.exceptions.exceptions import ExcecaoNaoAutorizado
from app.security.configuracao import ALGORITMO, CHAVE_SECRETA, MINUTOS_EXPIRACAO_TOKEN

def criar_token_acesso(usuario_id: int, email: str) -> str:
    agora = datetime.now(timezone.utc)
    conteudo = {
        "sub": str(usuario_id),
        "email": email,
        "iat": agora,
        "exp": agora + timedelta(minutes=MINUTOS_EXPIRACAO_TOKEN),
    }
    return jwt.encode(conteudo, CHAVE_SECRETA, algorithm=ALGORITMO)

def decodificar_token(token: str) -> dict:
    try:
        return jwt.decode(token, CHAVE_SECRETA, algorithms=[ALGORITMO])
    except jwt.ExpiredSignatureError as erro:
        raise ExcecaoNaoAutorizado("Token expirado") from erro
    except jwt.InvalidTokenError as erro:
        raise ExcecaoNaoAutorizado("Token inválido") from erro