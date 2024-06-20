from domain.models.documents.base_document import BaseDocument
from domain.models.banks.banks_types import Banks
from domain.models.repository import Repository


class BancolombiaRepository(Repository):

    def __init__(self):
        super().__init__()

    def get_one(self, structured, raw, code, rules):
        #  TODO: Replace this with API Calling querying bancolombia information
        entity = BaseDocument(structured, raw, code, rules, Banks.BANCOLOMBIA.value)
        return entity

    def get_multiple(self, structured, raw, docs_id, rules):
        entities = [BaseDocument(structured, raw, code, rules, Banks.BANCOLOMBIA.value) for code in docs_id]
        return entities
