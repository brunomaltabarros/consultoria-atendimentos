from app.models.consultor import Consultor
from app.dtos.consultor_dto import ConsultorDTO, ConsultorRespostaDTO 

class ConsultorMapper: 
    @staticmethod
    def para_dto_resposta(consultor: Consultor ) -> ConsultorRespostaDTO:
        return ConsultorRespostaDTO.model_validate(consultor)

    @staticmethod
    def para_modelo(dto: ConsultorDTO) -> Consultor:
        return Consultor(**dto.model_dump())
    
    @staticmethod
    def atualizar_modelo(consultor: Consultor, dto: ConsultorDTO) -> Consultor:
        for campo, valor in dto.model_dump().items():
            setattr(consultor, campo, valor)
        return consultor