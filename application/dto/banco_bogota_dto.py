class BancoBogotaDto:
    def __init__(self, metadata, code, rules):
        self._metadata = metadata
        self._code = code
        self._rules = rules

    @property
    def code(self):
        return self._code

    @property
    def metadata(self):
        return self._metadata

    @property
    def rules(self):
        return self._rules
