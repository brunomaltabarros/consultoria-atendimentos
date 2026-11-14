from sqlalchemy.orm import Session

from app.dtos.atendimento_dto import AtendimentoDTO
from app.mappers.atendimento_mapper import AtendimentoMapper
from app.models.atendimento import Atendimento
from app.repositories.atendimento_repository import AtendimentoRepositorio

class AtendimentoServico:
    def __init__(self, sessao: Session):
        self.repositorio = AtendimentoRepositorio(sessao)

    def listar(self, consultor_id: int | None = None, skip: int = 0, limit: int = 100) -> list[Atendimento]:
        return self.repositorio.listar(consultor_id=consultor_id, skip=skip, limit=limit)

    def buscar_por_id(self, atendimento_id: int) -> Atendimento:
        return self.repositorio.buscar_por_id(atendimento_id)

    def criar(self, dto: AtendimentoDTO) -> Atendimento:
        self.repositorio.validar_consultor_existe(dto.consultor_id)
        return self.repositorio.criar(AtendimentoMapper.para_modelo(dto))
    
    def atualizar(self, atendimento_id: int, dto: AtendimentoDTO) -> Atendimento:
        self.repositorio.validar_consultor_existe(dto.consultor_id)
        atendimento = self.repositorio.buscar_por_id(atendimento_id)
        atendimento = AtendimentoMapper.atualizar_modelo(atendimento, dto)
        return self.repositorio.atualizar(atendimento)

    def remover(self, atendimento_id: int) -> None:
        atendimento = self.repositorio.buscar_por_id(atendimento_id)
        self.repositorio.remover(atendimento)