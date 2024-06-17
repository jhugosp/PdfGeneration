from domain.models.rules.rule import Rule
from domain.models.documents.base_document import BaseDocument


class FirstRule(Rule):

    def __init__(self, document: BaseDocument, prompt, rule_type, rule_id, comments, version, status, description):
        super().__init__(document, prompt, rule_type, rule_id, comments, version, status, description)

    def validate(self):
        # TODO: initializer method
        pass

    def validate_by_code(self):
        # TODO: develop logic based on rule_type and description/code
        pass
