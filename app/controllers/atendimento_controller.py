from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import obter_sessao
from app.dtos.respostas_comuns import RESPOSTA_404
from app.dtos.atendimento_dto import AtendimentoDTO, AtendimentoRespostaDTO
from app.mappers.atendimento_mapper import AtendimentoMapper
from app.services.atendimento_service import AtendimentoServico

rotas = APIRouter(prefix="/atendimentos", tags=["Atendimentos"])

@rotas.get(
    "",
    response_model=list[AtendimentoRespostaDTO],
    summary="Listar atendimentos",
    description="Devolve a lista paginada de atendimentos. Pode ser filtrada por consultor_id.",
)
def listar_atendimentos(
    consultor_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
    sessao: Session = Depends(obter_sessao),
):
    atendimentos = AtendimentoServico(sessao).listar(consultor_id=consultor_id, skip=skip, limit=limit)
    return [AtendimentoMapper.para_dto_resposta(atendimento) for atendimento in atendimentos]

@rotas.get(
    "/{atendimento_id}",
    response_model=AtendimentoRespostaDTO,
    summary="Obter atendimento por ID",
    description="Devolve um atendimento específico.",
    responses={**RESPOSTA_404},
)
def obter_atendimento(atendimento_id: int, sessao: Session = Depends(obter_sessao)):
    atendimento = AtendimentoServico(sessao).buscar_por_id(atendimento_id)
    return AtendimentoMapper.para_dto_resposta(atendimento)

@rotas.post(
    "",
    response_model=AtendimentoRespostaDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar atendimento",
    description="Cria um atendimento vinculado a um consultor existente.",
    responses={**RESPOSTA_404},
)
def criar_atendimento(dto: AtendimentoDTO, sessao: Session = Depends(obter_sessao)):
    atendimento = AtendimentoServico(sessao).criar(dto)
    return AtendimentoMapper.para_dto_resposta(atendimento)

@rotas.put(
    "/{atendimento_id}",
    response_model=AtendimentoRespostaDTO,
    summary="Atualizar atendimento",
    description="Atualiza um atendimento. O consultor informado precisa existir.",
    responses={**RESPOSTA_404},
)
def atualizar_atendimento(atendimento_id: int, dto: AtendimentoDTO, sessao: Session = Depends(obter_sessao)):
    atendimento = AtendimentoServico(sessao).atualizar(atendimento_id, dto)
    return AtendimentoMapper.para_dto_resposta(atendimento)

@rotas.delete(
    "/{atendimento_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remover atendimento",
    description="Remove um atendimento do histórico.",
    responses={**RESPOSTA_404},
)
def remover_atendimento(atendimento_id: int, sessao: Session = Depends(obter_sessao)):
    AtendimentoServico(sessao).remover(atendimento_id)