from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dtos.consultor_dto import ConsultorDTO, ConsultorResponseDTO
from app.mappers.consultor_mapper import ConsultorMapper
from app.repositories.consultor_repository import ConsultorRepository

router = APIRouter(prefix="/consultores", tags=["Consultores"])

@router.get("", response_model=list[ConsultorResponseDTO])
def listar_consultores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    consultores = ConsultorRepository(db).get_all(skip=skip, limit=limit)
    return [ConsultorMapper.to_response_dto(consultor) for consultor in consultores]

@router.get("/{consultor_id}", response_model=ConsultorResponseDTO)
def obter_consultor(consultor_id: int, db: Session = Depends(get_db)):
    consultor = ConsultorRepository(db).get_by_id(consultor_id)
    return ConsultorMapper.to_response_dto(consultor)

@router.post("", response_model=ConsultorResponseDTO, status_code=status.HTTP_201_CREATED)
def criar_consultor(dto: ConsultorDTO, db: Session = Depends(get_db)):
    consultor = ConsultorMapper.to_model(dto)
    consultor = ConsultorRepository(db).create(consultor)
    return ConsultorMapper.to_response_dto(consultor)

@router.put("/{consultor_id}", response_model=ConsultorResponseDTO)
def atualizar_consultor(consultor_id: int, dto: ConsultorDTO, db: Session = Depends(get_db)):
    repository = ConsultorRepository(db)
    consultor = repository.get_by_id(consultor_id)
    consultor = ConsultorMapper.update_model(consultor, dto)
    consultor = repository.update(consultor)
    return ConsultorMapper.to_response_dto(consultor)

@router.delete("/{consultor_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_consultor(consultor_id: int, db: Session = Depends(get_db)):
    repository = ConsultorRepository(db)
    consultor = repository.get_by_id(consultor_id)
    repository.delete(consultor)