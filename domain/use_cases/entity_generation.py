from domain.models.documents.bancolombia_model import Bancolombia


class EntityGenerator:
    def __init__(self):
        pass

    @staticmethod
    def generate_entity():
        #  TODO: correctly generate document based on bank
        return Bancolombia()  # Need to unify with abstract class
