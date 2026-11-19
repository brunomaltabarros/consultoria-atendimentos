from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import obter_sessao
from app.dtos.respostas_comuns import RESPOSTA_401, RESPOSTA_403, RESPOSTA_404, RESPOSTA_409
from app.dtos.usuario_dto import UsuarioAtualizacaoDTO, UsuarioRespostaDTO
from app.mappers.usuario_mapper import UsuarioMapper
from app.models.usuario import Usuario
from app.security.dependencias import obter_usuario_logado
from app.services.usuario_service import UsuarioServico

rotas = APIRouter(prefix="/usuarios", tags=["Usuários"])

@rotas.get(
    "/",
    response_model=list[UsuarioRespostaDTO],
    summary="Listar usuários",
    description="Devolve a lista paginada de usuários cadastrados. Exige autenticação.",
    responses={**RESPOSTA_401},
)
def listar_usuarios(
    skip: int = 0,
    limit: int = 100,
    sessao: Session = Depends(obter_sessao),
    usuario_logado: Usuario = Depends(obter_usuario_logado),
):
    usuarios = UsuarioServico(sessao).listar(skip=skip, limit=limit)
    return [UsuarioMapper.para_dto_resposta(usuario) for usuario in usuarios]

@rotas.get(
    "/{usuario_id}",
    response_model=UsuarioRespostaDTO,
    summary="Obter usuário por ID",
    description="Devolve um usuário específico. Exige autenticação.",
    responses={**RESPOSTA_401, **RESPOSTA_404},
)
def obter_usuario(
    usuario_id: int,
    sessao: Session = Depends(obter_sessao),
    usuario_logado: Usuario = Depends(obter_usuario_logado),
):
    usuario = UsuarioServico(sessao).buscar_por_id(usuario_id)
    return UsuarioMapper.para_dto_resposta(usuario)

@rotas.put(
    "/{usuario_id}",
    response_model=UsuarioRespostaDTO,
    summary="Atualizar usuário",
    description="Atualiza nome e e-mail. Cada usuário só pode alterar os próprios dados.",
    responses={**RESPOSTA_401, **RESPOSTA_403, **RESPOSTA_404, **RESPOSTA_409},
)
def atualizar_usuario(
    usuario_id: int,
    usuario_dto: UsuarioAtualizacaoDTO,
    sessao: Session = Depends(obter_sessao),
    usuario_logado: Usuario = Depends(obter_usuario_logado),
):
    usuario = UsuarioServico(sessao).atualizar(usuario_id, usuario_dto, usuario_logado)
    return UsuarioMapper.para_dto_resposta(usuario)

@rotas.delete(
    "/{usuario_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remover usuário",
    description="Remove o usuário. Cada usuário só pode remover a própria conta.",
    responses={**RESPOSTA_401, **RESPOSTA_403, **RESPOSTA_404},
)
def remover_usuario(
    usuario_id: int,
    sessao: Session = Depends(obter_sessao),
    usuario_logado: Usuario = Depends(obter_usuario_logado),
):
    UsuarioServico(sessao).remover(usuario_id, usuario_logado)