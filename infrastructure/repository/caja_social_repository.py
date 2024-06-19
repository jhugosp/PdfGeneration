from domain.models.documents.caja_social_model import CajaSocial
from domain.models.repository import Repository


class CajaSocialRepository(Repository):
    def __init__(self):
        super().__init__()

    def get_one(self, code):
        #  TODO: Replace this with API Calling querying caja_social information
        entity = CajaSocial(code)
        return entity

    def get_multiple(self, docs_id):
        entities = [CajaSocial(code) for code in docs_id]
        return entities

    def get_all(self):
        entities = [CajaSocial(code) for code in range(10)]
        return entities
