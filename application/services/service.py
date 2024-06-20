from domain.models.repository import Repository
from application.data_handler.dto_generator import DtoGenerator


class Service:
    def __init__(self, dto_generator: DtoGenerator, repository: Repository):
        self._dto_generator = dto_generator
        self._repository = repository

    def get_one(self, structured, raw, doc_code, rules, bank_type):
        pass

    def get_multiple(self, structured, raw, doc_codes, rules, bank_type):
        pass
