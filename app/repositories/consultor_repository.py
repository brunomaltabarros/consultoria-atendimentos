from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions.exceptions import ExcecaoConflito, ExcecaoNaoEncontrado
from app.models.consultor import Consultor

class ConsultorRepositorio:
    def __init__(self, sessao: Session):
        self.sessao = sessao

    def listar(self,skip:int = 0, limit: int = 100) -> list[Consultor]:
        return self.sessao.query(Consultor).offset(skip).limit(limit).all()

    def buscar_por_id(self, consultor_id:int) -> Consultor:
        consultor = self.sessao.query(Consultor).filter(Consultor.id == consultor_id).first()
        if consultor is None:
            raise ExcecaoNaoEncontrado(f"Consultor {consultor_id} não encontrado")
        return consultor

    def criar(self, consultor: Consultor) -> Consultor:
        self.sessao.add(consultor)
        self._salvar()
        self.sessao.refresh(consultor)
        return consultor

    def atualizar(self, consultor: Consultor) -> Consultor:
        self._salvar()
        self.sessao.refresh(consultor)
        return consultor

    def remover(self, consultor: Consultor) -> None:
            self.sessao.delete(consultor)
            self._salvar()

    def _salvar(self) -> None:
        try:
            self.sessao.commit()
        except IntegrityError as erro:
            self.sessao.rollback()
            raise ExcecaoConflito("CPF ou e-mail já cadastrado para outro consultor") from erro