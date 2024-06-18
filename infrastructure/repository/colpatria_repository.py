from domain.models.documents.colpatria_model import Colpatria
from domain.models.repository import Repository


class ColpatriaRepository(Repository):
    def __init__(self):
        super().__init__()

    def get_one(self, code):
        #  TODO: Replace this with API Calling querying colpatria information
        entity = Colpatria(code)
        return entity
