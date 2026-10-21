from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import obter_sessao
from app.dtos.respostas_comuns import RESPOSTA_401, RESPOSTA_401_CREDENCIAIS, RESPOSTA_409
from app.dtos.usuario_dto import TokenDTO, UsuarioLoginDTO, UsuarioRegistroDTO, UsuarioRespostaDTO
from app.exceptions.exceptions import ExcecaoConflito, ExcecaoNaoAutorizado
from app.mappers.usuario_mapper import UsuarioMapper
from app.models.usuario import Usuario
from app.repositories.usuario_repository import UsuarioRepositorio
from app.security.dependencias import obter_usuario_logado
from app.security.senha import verificar_senha
from app.security.token import criar_token_acesso

rotas = APIRouter(prefix="/auth", tags=["Autenticação"])

@rotas.post(
    "/registrar",
    response_model=UsuarioRespostaDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar novo usuário",
    description="Cria um usuário com a senha armazenada como hash bcrypt. O e-mail precisa ser único.",
    responses={**RESPOSTA_409},
)
def registrar(dto: UsuarioRegistroDTO, sessao: Session = Depends(obter_sessao)):
    repositorio = UsuarioRepositorio(sessao)
    if repositorio.buscar_por_email(dto.email) is not None:
        raise ExcecaoConflito("E-mail já cadastrado.")
    usuario = repositorio.criar(UsuarioMapper.para_modelo(dto))
    return UsuarioMapper.para_dto_resposta(usuario)

@rotas.post(
    "/login",
    response_model=TokenDTO,
    summary="Autenticar e obter token JWT",
    description="Valida as credenciais e devolve um token JWT. A resposta é idêntica para senha incorreta e e-mail inexistente.",
    responses={**RESPOSTA_401_CREDENCIAIS},
)
def login(dto: UsuarioLoginDTO, sessao: Session = Depends(obter_sessao)):
    usuario = UsuarioRepositorio(sessao).buscar_por_email(dto.email)
    if usuario is None or not verificar_senha(dto.senha, usuario.senha_hash):
        raise ExcecaoNaoAutorizado("E-mail ou senha inválidos")
    if not usuario.ativo:
        raise ExcecaoNaoAutorizado("Usuário inativo")
    return TokenDTO(access_token=criar_token_acesso(usuario.id, usuario.email))

@rotas.get(
    "/eu",
    response_model=UsuarioRespostaDTO,
    summary="Dados do usuário autenticado",
    description="Devolve o usuário correspondente ao token enviado no cabeçalho Authorization.",
    responses={**RESPOSTA_401},
)
def quem_sou_eu(usuario: Usuario = Depends(obter_usuario_logado)):
    return UsuarioMapper.para_dto_resposta(usuario)