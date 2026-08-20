from pydantic import BaseModel, ConfigDict

class ConsultorDTO(BaseModel):
    nome: str
    cpf: str
    email: str
    telefone: str
    bio: str
    especialidade: str


class ConsultorResponseDTO(ConsultorDTO):
    id: int
    model_config = ConfigDict(from_attributes=True)