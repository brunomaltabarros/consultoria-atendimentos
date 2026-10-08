from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions.exceptions import ExcecaoConflito, ExcecaoNaoEncontrado
from app.models.usuario import Usuario

class UsuarioRepositorio:
    def __init__(self, sessao: Session):
        self.sessao = sessao

    def listar(self, skip: int = 0, limit: int = 100) -> list[Usuario]:
        return self.sessao.query(Usuario).offset(skip).limit(limit).all()

    def buscar_por_id(self, usuario_id: int) -> Usuario:
        usuario = self.sessao.query(Usuario).filter(Usuario.id == usuario_id).first()
        if usuario is None:
            raise ExcecaoNaoEncontrado(f"Usuário {usuario_id} não encontrado.")
        return usuario

    def buscar_por_email(self, email: str) -> Usuario | None:
        return self.sessao.query(Usuario).filter(Usuario.email == email).first()

    def criar(self, usuario: Usuario) -> Usuario:
        self.sessao.add(usuario)
        self._salvar()
        self.sessao.refresh(usuario)
        return usuario

    def _salvar(self) -> None:
        try:
            self.sessao.commit()
        except IntegrityError as erro:
            self.sessao.rollback()
            raise ExcecaoConflito("E-mail já cadastrado.") from erro