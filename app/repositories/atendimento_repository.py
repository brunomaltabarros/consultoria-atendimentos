from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions.exceptions import ExcecaoConflito, ExcecaoNaoEncontrado
from app.models.atendimento import Atendimento
from app.models.consultor import Consultor

class AtendimentoRepositorio:
    def __init__(self, sessao: Session):
        self.sessao = sessao

    def listar(self, consultor_id: int | None = None, skip: int = 0, limit: int = 100) -> list[Atendimento]:
        query = self.sessao.query(Atendimento)
        if consultor_id is not None:
            query = query.filter(Atendimento.consultor_id == consultor_id)
        return query.offset(skip).limit(limit).all()

    def buscar_por_id(self, atendimento_id: int) -> Atendimento:
        atendimento = self.sessao.query(Atendimento).filter(Atendimento.id == atendimento_id).first()
        if atendimento is None:
            raise ExcecaoNaoEncontrado(f"Atendimento {atendimento_id} não encontrado")
        return atendimento

    def validar_consultor_existe(self, consultor_id: int) -> None:
        existe = self.sessao.query(Consultor.id).filter(Consultor.id == consultor_id).first()
        if existe is None:
            raise ExcecaoNaoEncontrado(f"Consultor {consultor_id} não encontrado")

    def criar(self, atendimento: Atendimento) -> Atendimento:
         self.sessao.add(atendimento)
         self._salvar()
         self.sessao.refresh(atendimento)
         return atendimento

    def atualizar(self, atendimento: Atendimento) -> Atendimento:
             self._salvar()
             self.sessao.refresh(atendimento)
             return atendimento

    def remover(self, atendimento: Atendimento) -> None:
        self.sessao.delete(atendimento)
        self._salvar()

    def _salvar(self) -> None:
        try:
            self.sessao.commit()
        except IntegrityError as erro:
            self.sessao.rollback()
            raise ExcecaoConflito("Não foi possível salvar o atendimento") from erro