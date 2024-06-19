from domain.models.documents.bbva_model import Bbva
from domain.models.repository import Repository


class BbvaRepository(Repository):
    def __init__(self):
        super().__init__()

    def get_one(self, code):
        #  TODO: Replace this with API Calling querying bbva information
        entity = Bbva(code)
        return entity

    def get_multiple(self, docs_id):
        entities = [Bbva(code) for code in docs_id]
        return entities

    def get_all(self):
        entities = [Bbva(code) for code in range(10)]
        return entities
