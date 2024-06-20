from domain.models.banks.banks_types import Banks
from domain.models.documents.base_document import BaseDocument


class Repository:
    def __init__(self):
        self._banks_list = [Banks.BANCO_BOGOTA.value,
                            Banks.CAJA_SOCIAL.value,
                            Banks.BBVA.value,
                            Banks.BANCOLOMBIA.value,
                            Banks.COLPATRIA.value]

    def get_one(self, structured, raw, code, rules, bank):
        entity = {}
        if self.__validate_bank_type(bank):
            entity = BaseDocument(structured, raw, code, rules, bank)
        return entity

    def get_multiple(self, documents, bank):
        entities = []
        if self.__validate_bank_type(bank):
            entities = [BaseDocument(
                document.get("structured"),
                document.get("raw"),
                document.get("code"),
                document.get("rules"),
                bank) for document in documents]
        return entities

    def __validate_bank_type(self, bank):
        return bank in self._banks_list
