from domain.models.documents.bancolombia_model import Bancolombia
from application.dto.bancolombia_dto import BancolombiaDto


class DtoGenerator:

    def __init__(self):
        pass

    def generate_dto(self, entity: Bancolombia) -> BancolombiaDto:
        #   TODO: Generate a Dto object based on bank or generalize DTO
        #   Provisionally uses Bancolombia DTO, will make use of entity received from infrastructure layer
        dto = BancolombiaDto(entity.metadata, entity.code, entity.rules)
        return dto
