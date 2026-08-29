from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions import ConflictException, NotFoundException
from app.models.consultor import Consultor

class ConsultorRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self,skip:int = 0, limit: int = 100) -> list[Consultor]:
        return self.db.query(Consultor).offset(skip).limit(limit).all()

    def get_by_id(self, consultor_id:int) -> Consultor:
        consultor = self.db.query(Consultor).filter(Consultor.id == consultor_id).first()
        if consultor is None:
            raise NotFoundException(f"Consultor {consultor_id} não encontrado")
        return consultor

    def create(self, consultor: Consultor) -> Consultor:
        self.db.add(consultor)
        self._commit()
        self.db.refresh(consultor)
        return consultor

    def update(self, consultor: Consultor) -> Consultor:
        self._commit()
        self.db.refresh(consultor)
        return consultor

    def delete(self, consultor: Consultor) -> Consultor:
            self.db.delete(consultor)
            self._commit()

    def _commit(self) -> None:
        try:
            self.db.commit()
        except IntegrityError as exc:
            self.db.rollback()
            raise ConflictException("CPF ou e-mail já cadastrado para outro consultor") from exc
