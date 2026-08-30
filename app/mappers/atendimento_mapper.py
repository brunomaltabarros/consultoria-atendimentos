from app.models.atendimento import Atendimento
from app.dtos.atendimento_dto import AtendimentoDTO, AtendimentoResponseDTO

class AtendimentoMapper: 
    @staticmethod
    def to_response_dto(atendimento:Atendimento) -> AtendimentoResponseDTO:
        return AtendimentoResponseDTO.model_validate(atendimento)
    @staticmethod
    def to_model(dto: AtendimentoDTO) -> Atendimento:
        return Atendimento(**dto.model_dump())
    @staticmethod
    def update_model(atendimento: Atendimento, dto: AtendimentoDTO) -> Atendimento:
    for campo, valor in dto.model_dump().items():
        setattr(atendimento, campo, valor)
    return atendimento