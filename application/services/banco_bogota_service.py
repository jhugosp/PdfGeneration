from domain.models.repository import Repository
from application.data_handler.dto_generator import DtoGenerator
from application.services.service import Service


class BancoBogotaService(Service):
    def __init__(self, dto_generator: DtoGenerator, repository: Repository):
        super().__init__(dto_generator, repository)

    def get_one(self, structured, raw, doc_code, rules, bank_type):
        return self._dto_generator.generate_dto(self._repository.get_one(structured, raw, doc_code, rules, bank_type))

    def get_multiple(self, documents, bank_type):
        entities = self._repository.get_multiple(documents, bank_type)
        result = []
        for entity in entities:
            result.append(self._dto_generator.generate_dto(entity))
        return result
