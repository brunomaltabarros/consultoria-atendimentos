from sqlalchemy.orm import Session

from app.dtos.usuario_dto import UsuarioLoginDTO, UsuarioRegistroDTO
from app.exceptions.exceptions import ExcecaoNaoAutorizado
from app.models.usuario import Usuario
from app.repositories.usuario_repository import UsuarioRepositorio
from app.security.senha import verificar_senha
from app.security.token import criar_token_acesso
from app.services.usuario_service import UsuarioServico


class AuthServico:
    def __init__(self, sessao: Session):
        self.repositorio = UsuarioRepositorio(sessao)
        self.usuarios = UsuarioServico(sessao)

    def registrar(self, dto: UsuarioRegistroDTO) -> Usuario:
        return self.usuarios.criar(dto)

    def autenticar(self, dto: UsuarioLoginDTO) -> str:
        usuario = self.repositorio.buscar_por_email(dto.email)
        if usuario is None or not verificar_senha(dto.senha, usuario.senha_hash):
            raise ExcecaoNaoAutorizado("E-mail ou senha inválidos")
        if not usuario.ativo:
            raise ExcecaoNaoAutorizado("Usuário inativo")
        return criar_token_acesso(usuario.id, usuario.email)