from domain.models.rules.rule import Rule
from domain.models.documents.base_document import BaseDocument


class SecondRule(Rule):

    def __init__(self, document: BaseDocument, prompt, rule_type, rule_id, comments, version, status, description):
        super().__init__(document, prompt, rule_type, rule_id, comments, version, status, description)

    def validate(self):
        pass

    def validate_by_prompt(self):
        # TODO: Pass down prompt created to AI Model to process rule
        pass
