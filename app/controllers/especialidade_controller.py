from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import obter_sessao
from app.dtos.respostas_comuns import RESPOSTA_401, RESPOSTA_404, RESPOSTA_409
from app.dtos.especialidade_dto import (EspecialidadeComConsultoresDTO,EspecialidadeDTO,EspecialidadeRespostaDTO,)
from app.mappers.especialidade_mapper import EspecialidadeMapper
from app.models.usuario import Usuario
from app.security.dependencias import obter_usuario_logado
from app.services.especialidade_service import EspecialidadeServico

rotas = APIRouter(prefix="/especialidades", tags=["Especialidades"])

@rotas.get(
    "",
    response_model=list[EspecialidadeRespostaDTO],
    summary="Listar especialidades",
    description="Devolve a lista paginada de especialidades.",
)
def listar_especialidades(skip: int = 0, limit: int = 100, sessao: Session = Depends(obter_sessao)):
    especialidades = EspecialidadeServico(sessao).listar(skip=skip, limit=limit)
    return [EspecialidadeMapper.para_dto_resposta(e) for e in especialidades]

@rotas.get(
    "/{especialidade_id}",
    response_model=EspecialidadeComConsultoresDTO,
    summary="Obter especialidade com seus consultores",
    description="Devolve a especialidade e a lista de consultores vinculados a ela.",
    responses={**RESPOSTA_404},
)
def obter_especialidade(especialidade_id: int, sessao: Session = Depends(obter_sessao)):
    especialidade = EspecialidadeServico(sessao).buscar_por_id(especialidade_id)
    return EspecialidadeMapper.para_dto_com_consultores(especialidade)

@rotas.post(
    "",
    response_model=EspecialidadeRespostaDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar especialidade",
    description="Cria uma especialidade. O nome precisa ser único. Exige autenticação.",
    responses={**RESPOSTA_401, **RESPOSTA_409},
)
def criar_especialidade(
    dto: EspecialidadeDTO,
    sessao: Session = Depends(obter_sessao),
    usuario_logado: Usuario = Depends(obter_usuario_logado),
):
    especialidade = EspecialidadeServico(sessao).criar(dto)
    return EspecialidadeMapper.para_dto_resposta(especialidade)

@rotas.put(
    "/{especialidade_id}",
    response_model=EspecialidadeRespostaDTO,
    summary="Atualizar especialidade",
    description="Atualiza nome e descrição. Exige autenticação.",
    responses={**RESPOSTA_401, **RESPOSTA_404, **RESPOSTA_409},
)
def atualizar_especialidade(
    especialidade_id: int,
    dto: EspecialidadeDTO,
    sessao: Session = Depends(obter_sessao),
    usuario_logado: Usuario = Depends(obter_usuario_logado),
):
    especialidade = EspecialidadeServico(sessao).atualizar(especialidade_id, dto)
    return EspecialidadeMapper.para_dto_resposta(especialidade)

@rotas.delete(
    "/{especialidade_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remover especialidade",
    description="Remove uma especialidade. Exige autenticação.",
    responses={**RESPOSTA_401, **RESPOSTA_404},
)
def remover_especialidade(
    especialidade_id: int,
    sessao: Session = Depends(obter_sessao),
    usuario_logado: Usuario = Depends(obter_usuario_logado),
):
    EspecialidadeServico(sessao).remover(especialidade_id)

@rotas.post(
    "/{especialidade_id}/consultores/{consultor_id}",
    response_model=EspecialidadeComConsultoresDTO,
    summary="Vincular consultor a uma especialidade",
    description="Cria o vínculo n:n entre consultor e especialidade. Exige autenticação.",
    responses={**RESPOSTA_401, **RESPOSTA_404, **RESPOSTA_409},
)
def vincular_consultor(
    especialidade_id: int,
    consultor_id: int,
    sessao: Session = Depends(obter_sessao),
    usuario_logado: Usuario = Depends(obter_usuario_logado),
):
    especialidade = EspecialidadeServico(sessao).vincular_consultor(especialidade_id, consultor_id)
    return EspecialidadeMapper.para_dto_com_consultores(especialidade)

@rotas.delete(
    "/{especialidade_id}/consultores/{consultor_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Desvincular consultor de uma especialidade",
    description="Remove o vínculo entre consultor e especialidade. Exige autenticação.",
    responses={**RESPOSTA_401, **RESPOSTA_404},
)
def desvincular_consultor(
    especialidade_id: int,
    consultor_id: int,
    sessao: Session = Depends(obter_sessao),
    usuario_logado: Usuario = Depends(obter_usuario_logado),
):
    EspecialidadeServico(sessao).desvincular_consultor(especialidade_id, consultor_id)