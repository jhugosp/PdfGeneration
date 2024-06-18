from typing import Type

from domain.models.documents.base_document import BaseDocument
from domain.models.banks.banks_types import Banks
from application.dto.bancolombia_dto import BancolombiaDto
from application.dto.bbva_dto import BbvaDto
from application.dto.colpatria_dto import ColpatriaDto
from application.dto.caja_social_dto import CajaSocialDto
from application.dto.banco_bogota_dto import BancoBogotaDto


class DtoGenerator:

    def __init__(self):
        self._type_mapping = {
            Banks.BANCOLOMBIA.value: BancolombiaDto,
            Banks.BBVA.value: BbvaDto,
            Banks.COLPATRIA.value: ColpatriaDto,
            Banks.CAJA_SOCIAL.value: CajaSocialDto,
            Banks.BANCO_BOGOTA.value: BancoBogotaDto
        }

    def _get_dto_class(self, bank_type: str):
        try:
            return self._type_mapping.get(bank_type)
        except KeyError:
            raise ValueError(f"Bank type {bank_type} is not valid")

    def generate_dto(self, entity: BaseDocument, bank_type: str):
        #   TODO: Generate a Dto object based on bank or generalize DTO
        dto_class = self._get_dto_class(bank_type)
        dto = dto_class(entity.metadata, entity.code, entity.rules)

        return dto
