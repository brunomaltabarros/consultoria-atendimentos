from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dtos.atendimento_dto import AtendimentoDTO, AtendimentoResponseDTO
from app.mappers.atendimento_mapper import AtendimentoMapper
from app.repositories.atendimento_repository import AtendimentoRepository

router = APIRouter(prefix="/atendimentos", tags=["Atendimentos"])

@router.get("", response_model=list[AtendimentoResponseDTO])
def listar_atendimentos(
    consultor_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    atendimentos = AtendimentoRepository(db).get_all(consultor_id=consultor_id, skip=skip, limit=limit)
    return [AtendimentoMapper.to_response_dto(atendimento) for atendimento in atendimentos]

@router.get("/{atendimento_id}", response_model=AtendimentoResponseDTO)
def obter_atendimento(atendimento_id: int, db: Session = Depends(get_db)):
    atendimento = AtendimentoRepository(db).get_by_id(atendimento_id)
    return AtendimentoMapper.to_response_dto(atendimento)

@router.post("", response_model=AtendimentoResponseDTO, status_code=status.HTTP_201_CREATED)
def criar_atendimento(dto: AtendimentoDTO, db: Session = Depends(get_db)):
    repository = AtendimentoRepository(db)
    repository.ensure_consultor_exists(dto.consultor_id)
    atendimento = AtendimentoMapper.to_model(dto)
    atendimento = repository.create(atendimento)
    return AtendimentoMapper.to_response_dto(atendimento)

@router.put("/{atendimento_id}", response_model=AtendimentoResponseDTO)
def atualizar_atendimento(atendimento_id: int, dto: AtendimentoDTO, db: Session = Depends(get_db)):
    repository = AtendimentoRepository(db)
    repository.ensure_consultor_exists(dto.consultor_id)
    atendimento = repository.get_by_id(atendimento_id)
    atendimento = AtendimentoMapper.update_model(atendimento, dto)
    atendimento = repository.update(atendimento)
    return AtendimentoMapper.to_response_dto(atendimento)

@router.delete("/{atendimento_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_atendimento(atendimento_id: int, db: Session = Depends(get_db)):
    repository = AtendimentoRepository(db)
    atendimento = repository.get_by_id(atendimento_id)
    repository.delete(atendimento)