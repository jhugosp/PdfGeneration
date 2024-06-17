from abc import ABC, abstractmethod
from domain.models.result import Result
from domain.models.documents.base_document import BaseDocument


class Rule(ABC):

    def __init__(self, document: BaseDocument, prompt, rule_type, rule_id, comments, version, status, description):
        self._document = document
        self._prompt = prompt
        self._type = rule_type
        self._id = rule_id
        self._comments = comments
        self._version = version
        self._status = status
        self._description = description
        self._result = None

    @property
    def result(self):
        return self._result

    @property
    def description(self):
        return self._description

    @property
    def status(self):
        return self._status

    @property
    def version(self):
        return self._version

    @property
    def comments(self):
        return self._comments

    @property
    def rule_id(self):
        return self._id

    @property
    def rule_type(self):
        return self._type

    @property
    def prompt(self):
        return self._prompt

    @property
    def document(self):
        return self._document

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
    def prepare_prompt(self):
        pass
