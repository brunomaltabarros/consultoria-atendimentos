from datetime import datetime
from pydantic import BaseModel, ConfigDict

class AtendimentoDTO(BaseModel):
    consultor_id: int
    cliente_nome: str
    data_atendimento: datetime
    descricao: str 
    tipo: str

class AtendimentoRespostaDTO(AtendimentoDTO):
    id:int
    model_config = ConfigDict(from_attributes=True)