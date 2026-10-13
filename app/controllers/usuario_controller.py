from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import obter_sessao
from app.dtos.usuario_dto import UsuarioAtualizacaoDTO, UsuarioRespostaDTO
from app.exceptions.exceptions import ExcecaoConflito, ExcecaoProibido
from app.mappers.usuario_mapper import UsuarioMapper
from app.models.usuario import Usuario
from app.repositories.usuario_repository import UsuarioRepositorio
from app.security.dependencias import obter_usuario_logado

rotas = APIRouter(prefix="/usuarios", tags=["Usuários"])

def garantir_proprio_usuario(usuario_id: int, usuario_logado: Usuario) -> None:
    if usuario_id != usuario_logado.id:
        raise ExcecaoProibido("Você só pode alterar seus próprios dados.")

@rotas.get("/", response_model=list[UsuarioRespostaDTO])
def listar_usuarios(
    skip: int = 0,
    limit: int = 100,
    sessao: Session = Depends(obter_sessao),
    usuario_logado: Usuario = Depends(obter_usuario_logado),
):
    usuarios = UsuarioRepositorio(sessao).listar(skip=skip, limit=limit)
    return [UsuarioMapper.para_dto_resposta(usuario) for usuario in usuarios]

@rotas.get("/{usuario_id}", response_model=UsuarioRespostaDTO)
def obter_usuario(
    usuario_id: int,
    sessao: Session = Depends(obter_sessao),
    usuario_logado: Usuario = Depends(obter_usuario_logado),
):
    usuario = UsuarioRepositorio(sessao).buscar_por_id(usuario_id)
    return UsuarioMapper.para_dto_resposta(usuario)

@rotas.put("/{usuario_id}", response_model=UsuarioRespostaDTO)
def atualizar_usuario(
    usuario_id: int,
    usuario_dto: UsuarioAtualizacaoDTO,
    sessao: Session = Depends(obter_sessao),
    usuario_logado: Usuario = Depends(obter_usuario_logado),
):
    garantir_proprio_usuario(usuario_id, usuario_logado)
    repositorio = UsuarioRepositorio(sessao)
    usuario = repositorio.buscar_por_id(usuario_id)
    existente = repositorio.buscar_por_email(usuario_dto.email)
    if existente is not None and existente.id != usuario_id:
        raise ExcecaoConflito("O email fornecido já está em uso por outro usuário.")
    usuario = UsuarioMapper.atualizar_modelo(usuario, usuario_dto)
    usuario = repositorio.atualizar(usuario)
    return UsuarioMapper.para_dto_resposta(usuario)

@rotas.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_usuario(
    usuario_id: int,
    sessao: Session = Depends(obter_sessao),
    usuario_logado: Usuario = Depends(obter_usuario_logado),
):
    garantir_proprio_usuario(usuario_id, usuario_logado)
    repositorio = UsuarioRepositorio(sessao)
    usuario = repositorio.buscar_por_id(usuario_id)
    repositorio.remover(usuario)
