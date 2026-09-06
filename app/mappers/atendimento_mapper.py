from app.models.atendimento import Atendimento
from app.dtos.atendimento_dto import AtendimentoDTO, AtendimentoRespostaDTO

class AtendimentoMapper: 
    @staticmethod
    def para_dto_resposta(atendimento: Atendimento) -> AtendimentoRespostaDTO:
        return AtendimentoRespostaDTO.model_validate(atendimento)

    @staticmethod
    def para_modelo(dto: AtendimentoDTO) -> Atendimento:
        return Atendimento(**dto.model_dump())

    @staticmethod
    def atualizar_modelo(atendimento: Atendimento, dto: AtendimentoDTO) -> Atendimento:
        for campo, valor in dto.model_dump().items():
            setattr(atendimento, campo, valor)
        return atendimento