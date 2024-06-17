from domain.models.result import Result
from domain.models.documents.base_document import BaseDocument


class Rule():

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

    def validate(self):
        pass

    def validate_by_prompt(self):
        pass

    def validate_by_code(self):
        pass

    def prepare_prompt_input(self):
        # TODO: create input based on received parameters coming from rules DB
        pass

    def process_prompt_response(self):
        # TODO: Manage response to create report
        pass
