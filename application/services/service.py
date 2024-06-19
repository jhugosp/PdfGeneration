from domain.models.repository import Repository
from application.data_handler.dto_generator import DtoGenerator


class Service:
    def __init__(self, dto_generator: DtoGenerator, repository: Repository):
        self._dto_generator = dto_generator
        self._repository = repository

    def get_one(self, doc_code, bank_type):
        pass

    def get_all(self, bank_type):
        pass

    def get_multiple(self, doc_codes, bank_type):
        pass
