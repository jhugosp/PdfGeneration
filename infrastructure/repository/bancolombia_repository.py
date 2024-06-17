from domain.models.documents.bancolombia_model import Bancolombia
from domain.models.repository import Repository


class BancolombiaRepository(Repository):

    def __init__(self):
        super().__init__()

    def get_one(self, code):
        #  TODO: Replace this with DB instance and query
        entity = Bancolombia(code)
        return entity
