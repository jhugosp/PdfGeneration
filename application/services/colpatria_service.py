from domain.models.repository import Repository
from application.data_handler.dto_generator import DtoGenerator
from application.services.service import Service


class ColpatriaService(Service):
    def __init__(self, dto_generator: DtoGenerator, repository: Repository):
        super().__init__(dto_generator, repository)

    def get_one(self, doc_code, bank_type):
        return self._dto_generator.generate_dto(self._repository.get_one(doc_code), bank_type)

    def get_multiple(self, doc_codes, bank_type):
        entities = self._repository.get_multiple(doc_codes)
        result = []
        for entity in entities:
            result.append(self._dto_generator.generate_dto(entity, bank_type))
        return result

    def get_all(self, bank_type):
        entities = self._repository.get_all()
        result = []
        for entity in entities:
            result.append(self._dto_generator.generate_dto(entity, bank_type))
        return result
