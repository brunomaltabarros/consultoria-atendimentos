from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.database import obter_sessao
from app.exceptions.exceptions import ExcecaoNaoAutorizado, ExcecaoNaoEncontrado
from app.models.usuario import Usuario
from app.repositories.usuario_repository import UsuarioRepositorio
from app.security.token import decodificar_token

esquema_bearer = HTTPBearer(auto_error=False)

def obter_usuario_logado(
        crendencial: HTTPAuthorizationCredentials | None = Depends(esquema_bearer),
        sessao: Session = Depends(obter_sessao),
) -> Usuario:
    if crendencial is None:
        raise ExcecaoNaoAutorizado("Token de autenticação não fornecido.")

    conteudo = decodificar_token(crendencial.credentials)
    usuario_id = conteudo.get("sub")
    if usuario_id is None:
        raise ExcecaoNaoAutorizado("Token sem identificação de usuário.") 

    try:
        usuario = UsuarioRepositorio(sessao).buscar_por_id(int(usuario_id))
    except ExcecaoNaoEncontrado as erro:
        raise ExcecaoNaoAutorizado("Usuário do token não existe mais") from erro
    if not usuario.ativo:
        raise ExcecaoNaoAutorizado("Usuário inativo.")
    
    return usuario