from domain.models.documents.base_document import BaseDocument
from domain.models.banks.banks_types import Banks
from application.dto.bancolombia_dto import BancolombiaDto
from application.dto.bbva_dto import BbvaDto
from application.dto.colpatria_dto import ColpatriaDto
from application.dto.caja_social_dto import CajaSocialDto
from application.dto.banco_bogota_dto import BancoBogotaDto


class DtoGenerator:

    def __init__(self):
        pass

    def generate_dto(self, entity: BaseDocument, bank_type: Banks):
        #   TODO: Generate a Dto object based on bank or generalize DTO
        dto = None
        match bank_type:
            case Banks.BANCOLOMBIA:
                dto = BancolombiaDto(entity.metadata, entity.code, entity.rules)
            case Banks.BBVA:
                dto = BbvaDto(entity.metadata, entity.code, entity.rules)
            case Banks.COLPATRIA:
                dto = ColpatriaDto(entity.metadata, entity.code, entity.rules)
            case Banks.CAJA_SOCIAL:
                dto = CajaSocialDto(entity.metadata, entity.code, entity.rules)
            case Banks.BANCO_BOGOTA:
                dto = BancoBogotaDto(entity.metadata, entity.code, entity.rules)
            case _:
                print("Bank not valid")

        return dto
