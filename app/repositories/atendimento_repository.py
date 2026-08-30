from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions.exceptions import ConflictException, NotFoundException
from app.models.atendimento import Atendimento
from app.models.consultor import Consultor

class AtendimentoRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self, consultor_id: int | None = None, skip: int = 0, limit: int = 100) -> list[Atendimento]:
        query = self.db.query(Atendimento)
        if consultor_id is not None:
            query = query.filter(Atendimento.consultor_id == consultor_id)
        return query.offset(skip).limit(limit).all()

    def get_by_id(self, atendimento_id: int) -> Atendimento:
        atendimento = self.db.query(Atendimento).filter(Atendimento.id == atendimento_id).first()
        if atendimento is None:
            raise NotFoundException(f"Atendimento {atendimento_id} não encontrado")
        return atendimento

    def ensure_consultor_exists(self, consultor_id: int) -> None:
        existe = self.db.query(Consultor.id).filter(Consultor.id == consultor_id).first()
        if existe is None:
            raise NotFoundException(f"Consultor {consultor_id} não encontrado")
    
    def create(self, atendimento: Atendimento) -> Atendimento:
         self.db.add(atendimento)
         self._commit()
         self.db.refresh(atendimento)
         return atendimento

    def update(self, atendimento: Atendimento) -> Atendimento:
             self._commit()
             self.db.refresh(atendimento)
             return atendimento

    def delete(self, atendimento: Atendimento) -> None:
        self.db.delete(atendimento)
        self._commit()
    
    def _commit(self) -> None:
        try:
            self.db.commit()
        except IntegrityError as exc:
            self.db.rollback()
            raise ConflictException("Não foi possível salvar o atendimento") from exc