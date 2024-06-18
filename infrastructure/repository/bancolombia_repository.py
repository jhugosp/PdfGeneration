from domain.models.documents.bancolombia_model import Bancolombia
from domain.models.repository import Repository


class BancolombiaRepository(Repository):

    def __init__(self):
        super().__init__()

    def get_one(self, code):
        #  TODO: Replace this with API Calling querying bancolombia information
        entity = Bancolombia(code)
        return entity
