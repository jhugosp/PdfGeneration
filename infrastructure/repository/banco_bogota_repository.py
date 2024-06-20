from domain.models.documents.base_document import BaseDocument
from domain.models.repository import Repository
from domain.models.banks.banks_types import Banks


class BancoBogotaRepository(Repository):
    def __init__(self):
        super().__init__()

    def get_one(self, structured, raw, code, rules):
        #  TODO: Replace this with API Calling querying b_bogota information
        entity = BaseDocument(structured, raw, code, rules, Banks.BANCO_BOGOTA.value)
        return entity

    def get_multiple(self, structured, raw, docs_id, rules):
        entities = [BaseDocument(structured, raw, code, rules, Banks.BANCO_BOGOTA.value) for code in docs_id]
        return entities
