class BaseDocument:
    def __init__(self, structured_meta, raw_meta):
        self._structured_meta = structured_meta
        self._raw_meta = raw_meta
        self._rules = self.load_rules()
        self._config = {}

    @property
    def rules(self):
        return self._rules

    @property
    def config(self):
        return self._config

    def load_rules(self):
        #  TODO: consult dataset, retrieve document
        return []  # Init rules

    def run_validations(self):
        pass
