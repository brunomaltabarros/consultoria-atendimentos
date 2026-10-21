from pydantic import BaseModel, ConfigDict


class ErroRespostaDTO(BaseModel):
    model_config = ConfigDict(json_schema_extra={"example": {"erro": "Consultor não encontrado."}})

    erro: str