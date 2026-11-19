from sqlalchemy.orm import Session

from app.dtos.usuario_dto import UsuarioAtualizacaoDTO, UsuarioRegistroDTO
from app.exceptions.exceptions import ExcecaoConflito, ExcecaoProibido
from app.mappers.usuario_mapper import UsuarioMapper
from app.models.usuario import Usuario
from app.repositories.usuario_repository import UsuarioRepositorio

class UsuarioServico:
    def __init__(self, sessao: Session):
        self.repositorio = UsuarioRepositorio(sessao)

    def listar(self, skip: int = 0, limit: int = 100) -> list[Usuario]:
        return self.repositorio.listar(skip=skip, limit=limit)

    def buscar_por_id(self, usuario_id: int) -> Usuario:
        return self.repositorio.buscar_por_id(usuario_id)

    def criar(self, dto: UsuarioRegistroDTO) -> Usuario:
        self._garantir_email_disponivel(dto.email)
        return self.repositorio.criar(UsuarioMapper.para_modelo(dto))

    def atualizar(self, usuario_id: int, dto: UsuarioAtualizacaoDTO, solicitante: Usuario) -> Usuario:
        self._garantir_proprio_usuario(usuario_id, solicitante)
        usuario = self.repositorio.buscar_por_id(usuario_id)
        self._garantir_email_disponivel(dto.email, ignorar_id=usuario_id)
        usuario = UsuarioMapper.atualizar_modelo(usuario, dto)
        return self.repositorio.atualizar(usuario)

    def remover(self, usuario_id: int, solicitante: Usuario) -> None:
        self._garantir_proprio_usuario(usuario_id, solicitante)
        usuario = self.repositorio.buscar_por_id(usuario_id)
        self.repositorio.remover(usuario)

    def _garantir_proprio_usuario(self, usuario_id: int, solicitante: Usuario) -> None:
        if usuario_id != solicitante.id:
            raise ExcecaoProibido("Você não tem permissão para realizar esta ação.")

    def _garantir_email_disponivel(self, email: str, ignorar_id: int | None =  None) -> None:
        existente = self.repositorio.buscar_por_email(email)
        if existente is not None and existente.id != ignorar_id:
            raise ExcecaoConflito("O email já cadastrado.")
