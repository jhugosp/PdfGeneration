from domain.models.repository import Repository
from application.data_handler.dto_generator import DtoGenerator


class BancolombiaService:
    def __init__(self, dto_generator: DtoGenerator, repository: Repository):
        self._dto_generator = dto_generator
        self._repository = repository

    def get_one(self, doc_code):
        return self._dto_generator.generate_dto(self._repository.get_one(doc_code))
