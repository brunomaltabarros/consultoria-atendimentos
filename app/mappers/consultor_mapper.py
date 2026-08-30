from app.models.consultor import Consultor
from app.dtos.consultor_dto import ConsultorDTO, ConsultorResponseDTO 

class ConsultorMapper: 
    @staticmethod
    def to_response_dto(consultor: Consultor ) -> ConsultorResponseDTO:
        return ConsultorResponseDTO.model_validate(consultor)

    @staticmethod
    def to_model(dto: ConsultorDTO) -> Consultor:
        return Consultor(**dto.model_dump())
    
    @staticmethod
    def update_model(consultor: Consultor, dto: ConsultorDTO) -> Consultor:
        for campo, valor in dto.model_dump().items():
            setattr(consultor, campo, valor)
        return consultor