from sqlalchemy.orm import Session

from app.dtos.consultor_dto import ConsultorDTO
from app.mappers.consultor_mapper import ConsultorMapper
from app.models.consultor import Consultor 
from app.repositories.consultor_repository import ConsultorRepositorio

class ConsultorServico: 
    def __init__(self, sessao: Session):
        self.repositorio = ConsultorRepositorio(sessao)

    def listar(self, skip: int = 0, limit: int = 100) -> list[Consultor]:
        return self.repositorio.listar(skip=skip, limit=limit)

    def buscar_por_id(self, consultor_id: int) -> Consultor:
        return self.repositorio.buscar_por_id(consultor_id)

    def criar(self, dto: ConsultorDTO) -> Consultor:
        return self.repositorio.criar(ConsultorMapper.para_modelo(dto))

    def atualizar(self, consultor_id: int, dto: ConsultorDTO) -> Consultor:
        consultor = self.repositorio.buscar_por_id(consultor_id)
        consultor = ConsultorMapper.atualizar_modelo(consultor, dto)
        return self.repositorio.atualizar(consultor)

    def remover(self, consultor_id: int) -> None:
        consultor = self.repositorio.buscar_por_id(consultor_id)
        self.repositorio.remover(consultor)