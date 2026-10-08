from pydantic import BaseModel, ConfigDict, EmailStr, Field

class UsuarioRegistroDTO(BaseModel):
    nome: str = Field(min_length=3, max_length=120)
    email: EmailStr
    senha: str = Field(min_length=6, max_length=72)

class UsuarioLoginDTO(BaseModel):
    email: EmailStr
    senha: str

class UsuarioRespostaDTO(BaseModel):
    id: int
    nome: str
    email: EmailStr
    ativo: bool
    model_config = ConfigDict(from_attributes=True)

class TokenDTO(BaseModel):
    access_token: str
    token_type: str = "bearer"