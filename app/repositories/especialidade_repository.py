from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions.exceptions import ExcecaoConflito, ExcecaoNaoEncontrado
from app.models.especialidade import Especialidade

class EspecialidadeRepositorio:
    def __init__(self, sessao: Session):
        self.sessao = sessao

    def listar(self, skip: int = 0, limit: int = 100) -> list[Especialidade]:
        return self.sessao.query(Especialidade).offset(skip).limit(limit).all()

    def buscar_por_id(self, especialidade_id: int) -> Especialidade:
        especialidade = self.sessao.query(Especialidade).filter(Especialidade.id == especialidade_id).first()
        if especialidade is None:
            raise ExcecaoNaoEncontrado(f"Especialidade {especialidade_id} não encontrada")
        return especialidade

    def buscar_por_nome(self, nome: str) -> Especialidade | None:
        return self.sessao.query(Especialidade).filter(Especialidade.nome == nome).first()

    def criar(self, especialidade: Especialidade) -> Especialidade:
        self.sessao.add(especialidade)
        self._salvar()
        self.sessao.refresh(especialidade)
        return especialidade

    def atualizar(self, especialidade: Especialidade) -> Especialidade:
        self._salvar()
        self.sessao.refresh(especialidade)
        return especialidade

    def remover(self, especialidade: Especialidade) -> None:
        self.sessao.delete(especialidade)
        self._salvar()

    def _salvar(self) -> None:
        try:
            self.sessao.commit()
        except IntegrityError as erro:
            self.sessao.rollback()
            raise ExcecaoConflito("Já existe uma especialidade com esse nome") from erro