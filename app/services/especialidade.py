from sqlalchemy.orm import Session 

from app.dtos.especialidade_dto import EspecialidadeDTO
from app.exceptions.exceptions import ExcecaoConflito, ExcecaoNaoEncontrado
from app.mappers.especialidade_mapper import EspecialidadeMapper
from app.models.especialidade import Especialidade
from app.repositories.consultor_repository import ConsultorRepositorio
from app.repositories.especialidade_repository import EspecialidadeRepositorio

class EspecialidadeServico:
    def __init__(self, sessao: Session):
        self.repositorio = EspecialidadeRepositorio(sessao)
        self.consultores = ConsultorRepositorio(sessao)

    def listar(self, skip: int = 0, limit: int = 100) -> list[Especialidade]:
        return self.repositorio.listar(skip=skip, limit=limit)

    def buscar_por_id(self, especialidade_id: int) -> Especialidade:
        return self.repositorio.buscar_por_id(especialidade_id)

    def criar(self, dto: EspecialidadeDTO) -> Especialidade:
        self._garantir_nome_disponivel(dto.nome)
        return self.repositorio.criar(EspecialidadeMapper.para_modelo(dto))

    def atualizar(self, especialidade_id: int, dto: EspecialidadeDTO) -> Especialidade:
        especialidade = self.repositorio.buscar_por_id(especialidade_id)
        self._garantir_nome_disponivel(dto.nome, ignorar_id=especialidade_id)
        especialidade = EspecialidadeMapper.atualizar_modelo(especialidade, dto)
        return self.repositorio.atualizar(especialidade)

    def remover(self, especialidade_id: int) -> None:
        especialidade = self.repositorio.buscar_por_id(especialidade_id)
        self.repositorio.remover(especialidade)

    def vincular_consultor(self, especialidade_id: int, consultor_id: int) -> Especialidade:
        especialidade = self.repositorio.buscar_por_id(especialidade_id)
        consultor = self.consultores.buscar_por_id(consultor_id)
        if consultor in especialidade.consultores:
            raise ExcecaoConflito(f"Consultor {consultor_id} já possui essa especialidade")
        especialidade.consultores.append(consultor)
        return self.repositorio.atualizar(especialidade)

    def desvincular_consultor(self, especialidade_id: int, consultor_id: int) -> None:
        especialidade = self.repositorio.buscar_por_id(especialidade_id)
        consultor = self.consultores.buscar_por_id(consultor_id)
        if consultor not in especialidade.consultores:
            raise ExcecaoNaoEncontrado(f"Consultor {consultor_id} não possui essa especialidade")
        especialidade.consultores.remove(consultor)
        return self.repositorio.atualizar(especialidade)

    def _garantir_nome_disponivel(self, nome: str, ignorar_id: int | None = None) -> None:
        especialidade_existente = self.repositorio.buscar_por_nome(nome)
        if especialidade_existente is not None and especialidade_existente.id != ignorar_id:
            raise ExcecaoConflito(f"Especialidade com nome '{nome}' já existe.")