from pydantic import BaseModel, ConfigDict, Field

class EspecialidadeDTO(BaseModel):
    nome: str = Field(min_length=2, max_length=80)
    descricao: str | None = None

class EspecialidadeRespostaDTO(EspecialidadeDTO):
    id: int
    model_config = ConfigDict(from_attributes=True)

class ConsultorResumoDTO(BaseModel):
    id: int
    nome: str
    email: str
    model_config = ConfigDict(from_attributes=True)

class EspecialidadeComConsultoresDTO(EspecialidadeRespostaDTO):
    consultores: list[ConsultorResumoDTO] = []