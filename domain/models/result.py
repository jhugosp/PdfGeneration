class Result:
    def __init__(self, results):
        self._boolean_response = results[0]
        self._prompt_response = results[1]
        self._confidence_level = results[2]

    @property
    def boolean_response(self):
        return self._boolean_response

    @property
    def prompt_response(self):
        return self._prompt_response

    @property
    def confidence_level(self):
        return self._confidence_level
