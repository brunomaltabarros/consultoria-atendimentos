from pydantic import BaseModel, ConfigDict

class ConsultorDTO(BaseModel):
    nome: str
    cpf: str
    email: str
    telefone: str
    bio: str | None = None
    especialidade: str | None = None

class ConsultorRespostaDTO(ConsultorDTO):
    id: int
    model_config = ConfigDict(from_attributes=True)