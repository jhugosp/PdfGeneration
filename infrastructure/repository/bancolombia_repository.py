from domain.models.documents.bancolombia_model import Bancolombia
from domain.models.repository import Repository


class BancolombiaRepository(Repository):

    def __init__(self):
        super().__init__()

    def get_one(self, code):
        #  TODO: Replace this with API Calling querying bancolombia information
        entity = Bancolombia(code)
        return entity

    def get_multiple(self, docs_id):
        entities = [Bancolombia(code) for code in docs_id]
        return entities

    def get_all(self):
        entities = [Bancolombia(code) for code in range(10)]
        return entities
