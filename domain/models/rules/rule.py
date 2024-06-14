from abc import ABC, abstractmethod
from domain.models.result import Result


class Rule(ABC):

    def __init__(self, document, prompt_input):
        self.document = document
        self.prompt_input = prompt_input
        self._result = None

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, result: Result):
        self._result = result

    @abstractmethod
    def validate(self):
        pass

    @abstractmethod
    def validate_by_prompt(self):
        pass

    @abstractmethod
    def prepare_prompt_input(self):
        pass
