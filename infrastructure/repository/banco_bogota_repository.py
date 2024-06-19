from domain.models.documents.banco_bogota_model import BancoBogota
from domain.models.repository import Repository


class BancoBogotaRepository(Repository):
    def __init__(self):
        super().__init__()

    def get_one(self, code):
        #  TODO: Replace this with API Calling querying b_bogota information
        entity = BancoBogota(code)
        return entity

    def get_multiple(self, docs_id):
        entities = [BancoBogota(code) for code in docs_id]
        return entities

    def get_all(self):
        entities = [BancoBogota(code) for code in range(10)]
        return entities
