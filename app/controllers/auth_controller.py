from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import obter_sessao
from app.dtos.usuario_dto import TokenDTO, UsuarioLoginDTO, UsuarioRegistroDTO, UsuarioRespostaDTO
from app.exceptions.exceptions import ExcecaoConflito, ExcecaoNaoAutorizado
from app.mappers.usuario_mapper import UsuarioMapper
from app.models.usuario import Usuario
from app.repositories.usuario_repository import UsuarioRepositorio
from app.security.dependencias import obter_usuario_logado
from app.security.senha import verificar_senha
from app.security.token import criar_token_acesso

rotas = APIRouter(prefix="/auth", tags=["Autenticação"])

@rotas.post("/registrar", response_model=UsuarioRespostaDTO, status_code=status.HTTP_201_CREATED)
def registrar(dto: UsuarioRegistroDTO, sessao: Session = Depends(obter_sessao)):
    repositorio = UsuarioRepositorio(sessao)
    if repositorio.buscar_por_email(dto.email) is not None:
        raise ExcecaoConflito("E-mail já cadastrado.")
    usuario = repositorio.criar(UsuarioMapper.para_modelo(dto))
    return UsuarioMapper.para_dto_resposta(usuario)

@rotas.post("/login", response_model=TokenDTO)
def login(dto: UsuarioLoginDTO, sessao: Session = Depends(obter_sessao)):
    usuario = UsuarioRepositorio(sessao).buscar_por_email(dto.email)
    if usuario is None or not verificar_senha(dto.senha, usuario.senha_hash):
        raise ExcecaoNaoAutorizado("E-mail ou senha inválidos")
    if not usuario.ativo:
        raise ExcecaoNaoAutorizado("Usuário inativo")
    return TokenDTO(access_token=criar_token_acesso(usuario.id, usuario.email))

@rotas.get("/eu", response_model=UsuarioRespostaDTO)
def quem_sou_eu(usuario: Usuario = Depends(obter_usuario_logado)):
    return UsuarioMapper.para_dto_resposta(usuario)