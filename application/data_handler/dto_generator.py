from domain.use_cases.entity_generation import EntityGenerator
from application.dto.bancolombia_dto import BancolombiaDto


class DtoGenerator:

    def __init__(self, entity_generator: EntityGenerator):
        self.entity_generator = entity_generator
        pass

    def generate_dto(self) -> BancolombiaDto:
        #   TODO: Generate a Dto object based on bank
        entity = self.entity_generator.generate_entity()
        dto = BancolombiaDto(entity.rows, entity.summary, entity.account_state)
        return dto
