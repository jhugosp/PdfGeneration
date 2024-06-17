class BaseDocument:
    def __init__(self, structured_meta, raw_meta, code):
        self._code = code
        self._structured_meta = structured_meta
        self._raw_meta = raw_meta

    def load_rules(self):
        pass

    def run_validations(self):
        pass
