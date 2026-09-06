from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import obter_sessao
from app.dtos.atendimento_dto import AtendimentoDTO, AtendimentoRespostaDTO
from app.mappers.atendimento_mapper import AtendimentoMapper
from app.repositories.atendimento_repository import AtendimentoRepositorio

rotas = APIRouter(prefix="/atendimentos", tags=["Atendimentos"])

@rotas.get("", response_model=list[AtendimentoRespostaDTO])
def listar_atendimentos(
    consultor_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
    sessao: Session = Depends(obter_sessao),
):
    atendimentos = AtendimentoRepositorio(sessao).listar(consultor_id=consultor_id, skip=skip, limit=limit)
    return [AtendimentoMapper.para_dto_resposta(atendimento) for atendimento in atendimentos]

@rotas.get("/{atendimento_id}", response_model=AtendimentoRespostaDTO)
def obter_atendimento(atendimento_id: int, sessao: Session = Depends(obter_sessao)):
    atendimento = AtendimentoRepositorio(sessao).buscar_por_id(atendimento_id)
    return AtendimentoMapper.para_dto_resposta(atendimento)

@rotas.post("", response_model=AtendimentoRespostaDTO, status_code=status.HTTP_201_CREATED)
def criar_atendimento(dto: AtendimentoDTO, sessao: Session = Depends(obter_sessao)):
    repositorio = AtendimentoRepositorio(sessao)
    repositorio.validar_consultor_existe(dto.consultor_id)
    atendimento = AtendimentoMapper.para_modelo(dto)
    atendimento = repositorio.criar(atendimento)
    return AtendimentoMapper.para_dto_resposta(atendimento)

@rotas.put("/{atendimento_id}", response_model=AtendimentoRespostaDTO)
def atualizar_atendimento(atendimento_id: int, dto: AtendimentoDTO, sessao: Session = Depends(obter_sessao)):
    repositorio = AtendimentoRepositorio(sessao)
    repositorio.validar_consultor_existe(dto.consultor_id)
    atendimento = repositorio.buscar_por_id(atendimento_id)
    atendimento = AtendimentoMapper.atualizar_modelo(atendimento, dto)
    atendimento = repositorio.atualizar(atendimento)
    return AtendimentoMapper.para_dto_resposta(atendimento)

@rotas.delete("/{atendimento_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_atendimento(atendimento_id: int, sessao: Session = Depends(obter_sessao)):
    repositorio = AtendimentoRepositorio(sessao)
    atendimento = repositorio.buscar_por_id(atendimento_id)
    repositorio.remover(atendimento)