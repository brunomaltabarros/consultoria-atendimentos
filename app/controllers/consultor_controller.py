from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import obter_sessao
from app.dtos.respostas_comuns import RESPOSTA_404
from app.dtos.consultor_dto import ConsultorDTO, ConsultorRespostaDTO
from app.mappers.consultor_mapper import ConsultorMapper
from app.services.consultor_service import ConsultorServico

rotas = APIRouter(prefix="/consultores", tags=["Consultores"])

@rotas.get(
    "",
    response_model=list[ConsultorRespostaDTO],
    summary="Listar consultores",
    description="Devolve a lista paginada de consultores, com suas especialidades.",
)
def listar_consultores(skip: int = 0, limit: int = 100, sessao: Session = Depends(obter_sessao)):
    consultores = ConsultorServico(sessao).listar(skip=skip, limit=limit)
    return [ConsultorMapper.para_dto_resposta(consultor) for consultor in consultores]

@rotas.get(
    "/{consultor_id}",
    response_model=ConsultorRespostaDTO,
    summary="Obter consultor por ID",
    description="Devolve um consultor específico com suas especialidades.",
    responses={**RESPOSTA_404},
)
def obter_consultor(consultor_id: int, sessao: Session = Depends(obter_sessao)):
    consultor = ConsultorServico(sessao).buscar_por_id(consultor_id)
    return ConsultorMapper.para_dto_resposta(consultor)

@rotas.post(
    "",
    response_model=ConsultorRespostaDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar consultor",
    description="Cria um consultor. O e-mail e o CPF precisam ser únicos.",
)
def criar_consultor(dto: ConsultorDTO, sessao: Session = Depends(obter_sessao)):
    consultor = ConsultorServico(sessao).criar(dto)
    return ConsultorMapper.para_dto_resposta(consultor)

@rotas.put(
    "/{consultor_id}",
    response_model=ConsultorRespostaDTO,
    summary="Atualizar consultor",
    description="Atualiza os dados cadastrais de um consultor.",
    responses={**RESPOSTA_404},
)
def atualizar_consultor(consultor_id: int, dto: ConsultorDTO, sessao: Session = Depends(obter_sessao)):
    consultor = ConsultorServico(sessao).atualizar(consultor_id, dto)
    return ConsultorMapper.para_dto_resposta(consultor)

@rotas.delete(
    "/{consultor_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remover consultor",
    description="Remove um consultor do cadastro.",
    responses={**RESPOSTA_404},
)
def remover_consultor(consultor_id: int, sessao: Session = Depends(obter_sessao)):
    ConsultorServico(sessao).remover(consultor_id)