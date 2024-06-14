from domain.models.rules.rule import Rule


class FirstRule(Rule):

    def __init__(self):
        super().__init__()

    def validate_by_prompt(self):
        pass

    def validate(self):
        pass

    def prepare_prompt_input(self):
        pass

    def validate_by_code(self):
        pass
