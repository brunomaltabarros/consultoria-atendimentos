from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import obter_sessao
from app.dtos.respostas_comuns import RESPOSTA_401, RESPOSTA_404, RESPOSTA_409
from app.dtos.especialidade_dto import (EspecialidadeComConsultoresDTO,EspecialidadeDTO,EspecialidadeRespostaDTO,)
from app.exceptions.exceptions import ExcecaoConflito, ExcecaoNaoEncontrado
from app.mappers.especialidade_mapper import EspecialidadeMapper
from app.models.usuario import Usuario
from app.repositories.consultor_repository import ConsultorRepositorio
from app.repositories.especialidade_repository import EspecialidadeRepositorio
from app.security.dependencias import obter_usuario_logado

rotas = APIRouter(prefix="/especialidades", tags=["Especialidades"])

@rotas.get(
    "",
    response_model=list[EspecialidadeRespostaDTO],
    summary="Listar especialidades",
    description="Devolve a lista paginada de especialidades.",
)
def listar_especialidades(skip: int = 0, limit: int = 100, sessao: Session = Depends(obter_sessao)):
    especialidades = EspecialidadeRepositorio(sessao).listar(skip=skip, limit=limit)
    return [EspecialidadeMapper.para_dto_resposta(e) for e in especialidades]

@rotas.get(
    "/{especialidade_id}",
    response_model=EspecialidadeComConsultoresDTO,
    summary="Obter especialidade com seus consultores",
    description="Devolve a especialidade e a lista de consultores vinculados a ela.",
    responses={**RESPOSTA_404},
)
def obter_especialidade(especialidade_id: int, sessao: Session = Depends(obter_sessao)):
    especialidade = EspecialidadeRepositorio(sessao).buscar_por_id(especialidade_id)
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
    repositorio = EspecialidadeRepositorio(sessao)
    if repositorio.buscar_por_nome(dto.nome) is not None:
        raise ExcecaoConflito("Já existe uma especialidade com esse nome")
    especialidade = repositorio.criar(EspecialidadeMapper.para_modelo(dto))
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
    repositorio = EspecialidadeRepositorio(sessao)
    especialidade = repositorio.buscar_por_id(especialidade_id)
    existente = repositorio.buscar_por_nome(dto.nome)
    if existente is not None and existente.id != especialidade_id:
        raise ExcecaoConflito("Já existe uma especialidade com esse nome")
    especialidade = EspecialidadeMapper.atualizar_modelo(especialidade, dto)
    especialidade = repositorio.atualizar(especialidade)
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
    repositorio = EspecialidadeRepositorio(sessao)
    especialidade = repositorio.buscar_por_id(especialidade_id)
    repositorio.remover(especialidade)

@rotas.post(
    "/{especialidade_id}/consultores/{consultor_id}",
    response_model=EspecialidadeComConsultoresDTO,
    summary="Vincular consultor a uma especialidade",
    description="Cria o vínculo n:n entre consultor e especialidade. Exige autenticação.",
    responses={**RESPOSTA_401, **RESPOSTA_404, **RESPOSTA_409},
)
def vincular_consultor(especialidade_id: int,consultor_id: int,sessao: Session = Depends(obter_sessao),usuario_logado: Usuario = Depends(obter_usuario_logado),):
    repositorio = EspecialidadeRepositorio(sessao)
    especialidade = repositorio.buscar_por_id(especialidade_id)
    consultor = ConsultorRepositorio(sessao).buscar_por_id(consultor_id)
    if consultor in especialidade.consultores:
        raise ExcecaoConflito(f"Consultor {consultor_id} já possui essa especialidade")
    especialidade.consultores.append(consultor)
    especialidade = repositorio.atualizar(especialidade)
    return EspecialidadeMapper.para_dto_com_consultores(especialidade)

@rotas.delete(
    "/{especialidade_id}/consultores/{consultor_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Desvincular consultor de uma especialidade",
    description="Remove o vínculo entre consultor e especialidade. Exige autenticação.",
    responses={**RESPOSTA_401, **RESPOSTA_404},
)
def desvincular_consultor(especialidade_id: int,consultor_id: int,sessao: Session = Depends(obter_sessao),usuario_logado: Usuario = Depends(obter_usuario_logado),):
    repositorio = EspecialidadeRepositorio(sessao)
    especialidade = repositorio.buscar_por_id(especialidade_id)
    consultor = ConsultorRepositorio(sessao).buscar_por_id(consultor_id)
    if consultor not in especialidade.consultores:
        raise ExcecaoNaoEncontrado(f"Consultor {consultor_id} não possui essa especialidade")
    especialidade.consultores.remove(consultor)
    repositorio.atualizar(especialidade)