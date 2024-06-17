class BaseDocument:
    def __init__(self, structured_meta, raw_meta):
        self._structured_meta = structured_meta
        self._raw_meta = raw_meta

    def load_rules(self):
        pass

    def run_validations(self):
        pass
