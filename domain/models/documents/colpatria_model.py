from domain.models.documents.base_document import BaseDocument


class Colpatria(BaseDocument):

    def __init__(self):
        self.rows, self.summary, self.account_state = "rows", "summary", "account"
        self._rules = self.load_rules()

        structured_data = {
            "rows": self.rows,
            "summary": self.summary,
            "account_state": self.account_state
        }
        raw_data = {
            "data": [
                self.summary,
                self.account_state,
                self.rows
            ]
        }
        super().__init__(structured_data, raw_data)

    @property
    def rules(self):
        return self._rules

    def run_validations(self):
        #   Check banco colpatria validations
        pass

    def load_rules(self):
        #  TODO: consult dataset, retrieve document
        return []  # Init rules
