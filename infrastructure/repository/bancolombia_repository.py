from domain.models.repository import Repository


class BancolombiaRepository(Repository):

    def __init__(self):
        super().__init__()

    def get_one(self, structured, raw, code, rules, bank):
        return super().get_one(structured, raw, code, rules, bank)

    def get_multiple(self, documents, bank):
        return super().get_multiple(documents, bank)
