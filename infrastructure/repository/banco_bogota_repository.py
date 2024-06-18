from domain.models.documents.banco_bogota_model import BancoBogota
from domain.models.repository import Repository


class BancoBogotaRepository(Repository):
    def __init__(self):
        super().__init__()

    def get_one(self, code):
        #  TODO: Replace this with API Calling querying b_bogota information
        entity = BancoBogota(code)
        return entity
