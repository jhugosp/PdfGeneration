from domain.models.documents.base_document import BaseDocument


class CajaSocial(BaseDocument):

    def __init__(self, code):
        self._rules = self.load_rules()
        structured, raw = self._prepare_properties()

        super().__init__(structured, raw, code)

    @property
    def rules(self):
        return self._rules

    def run_validations(self):
        #   Check bancolombia validations
        pass

    def load_rules(self):
        #  TODO: consult dataset, retrieve document
        return []  # Init rules

    def _prepare_properties(self):
        structured_data = {
            "filed1": "something1",
            "field2": "something2",
            "field3": "something3"
        }
        raw_data = {
            "data": [
                "something1",
                "something2",
                "something3"
            ]
        }
        return structured_data, raw_data
