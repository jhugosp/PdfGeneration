from domain.models.documents.bbva_model import Bbva
from domain.models.repository import Repository


class BbvaRepository(Repository):
    def __init__(self):
        super().__init__()

    def get_one(self, code):
        #  TODO: Replace this with API Calling querying bbva information
        entity = Bbva(code)
        return entity
