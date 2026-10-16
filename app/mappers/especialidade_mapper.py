from app.dtos.especialidade_dto import (EspecialidadeComConsultoresDTO, EspecialidadeDTO, EspecialidadeRespostaDTO)
from app.models.especialidade import Especialidade

class EspecialidadeMapper:
    @staticmethod
    def para_dto_resposta(especialidade: Especialidade) -> EspecialidadeRespostaDTO:
        return EspecialidadeRespostaDTO.model_validate(especialidade)

    @staticmethod
    def para_dto_com_consultores(especialidade: Especialidade) -> EspecialidadeComConsultoresDTO:
        return EspecialidadeComConsultoresDTO.model_validate(especialidade)

    @staticmethod
    def para_modelo(dto: EspecialidadeDTO) -> Especialidade:
        return Especialidade(**dto.model_dump())

    @staticmethod
    def atualizar_modelo(modelo: Especialidade, dto: EspecialidadeDTO) -> Especialidade:
        modelo.nome = dto.nome
        modelo.descricao = dto.descricao
        return modelo