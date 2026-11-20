from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import obter_sessao
from app.dtos.respostas_comuns import RESPOSTA_401, RESPOSTA_401_CREDENCIAIS, RESPOSTA_409
from app.dtos.usuario_dto import TokenDTO, UsuarioLoginDTO, UsuarioRegistroDTO, UsuarioRespostaDTO
from app.mappers.usuario_mapper import UsuarioMapper
from app.models.usuario import Usuario
from app.security.dependencias import obter_usuario_logado
from app.services.auth_service import AuthServico

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
    usuario = AuthServico(sessao).registrar(dto)
    return UsuarioMapper.para_dto_resposta(usuario)

@rotas.post(
    "/login",
    response_model=TokenDTO,
    summary="Autenticar e obter token JWT",
    description="Valida as credenciais e devolve um token JWT. A resposta é idêntica para senha incorreta e e-mail inexistente.",
    responses={**RESPOSTA_401_CREDENCIAIS},
)
def login(dto: UsuarioLoginDTO, sessao: Session = Depends(obter_sessao)):
    token = AuthServico(sessao).autenticar(dto)
    return TokenDTO(access_token=token)

@rotas.get(
    "/eu",
    response_model=UsuarioRespostaDTO,
    summary="Dados do usuário autenticado",
    description="Devolve o usuário correspondente ao token enviado no cabeçalho Authorization.",
    responses={**RESPOSTA_401},
)
def quem_sou_eu(usuario: Usuario = Depends(obter_usuario_logado)):
    return UsuarioMapper.para_dto_resposta(usuario)