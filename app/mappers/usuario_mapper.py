from app.dtos.usuario_dto import UsuarioRegistroDTO, UsuarioRespostaDTO
from app.models.usuario import Usuario
from app.security.senha import gerar_hash_senha

class UsuarioMapper:
    @staticmethod
    def para_dto_resposta(usuario: Usuario) -> UsuarioRespostaDTO:
        return UsuarioRespostaDTO.model_validate(usuario)

    @staticmethod
    def para_modelo(dto: UsuarioRegistroDTO) -> Usuario:
        return Usuario(
            nome=dto.nome,
            email=dto.email,
            senha_hash=gerar_hash_senha(dto.senha),
            ativo=True,
        )
    