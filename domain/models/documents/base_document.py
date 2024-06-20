class BaseDocument:
    def __init__(self, structured_meta, raw_meta, code, rules, bank_type):
        self._code = code
        self._structured_meta = structured_meta
        self._raw_meta = raw_meta
        self._bank_type = bank_type
        self._rules = []

    @property
    def rules(self):
        return self._rules

    @property
    def code(self):
        return self._code

    @property
    def metadata(self):
        return self._structured_meta

    @property
    def bank_type(self):
        return self._bank_type

    def load_rules(self):
        pass

    def run_validations(self):
        pass

    @staticmethod
    def mock_rule_code():
        return {
            "prompt": "Some basic prompt",
            "rule_type": "code",
            "rule_id": 1,
            "comments": "some basic prompt",
            "version": 1.0,
            "status": True,
            "description": "Some basic description"
        }

    @staticmethod
    def mock_rule_prompt():
        return {
            "prompt": "Some basic prompt",
            "rule_type": "prompt",
            "rule_id": 1,
            "comments": "some basic prompt",
            "version": 1.0,
            "status": True,
            "description": "Some basic description"
        }
