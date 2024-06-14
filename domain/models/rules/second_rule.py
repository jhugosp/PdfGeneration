from domain.models.rules.rule import Rule


class SecondRule(Rule):

    def __init__(self):
        super().__init__()

    def validate_by_prompt(self):
        pass

    def validate(self):
        pass

    def prepare_prompt_input(self):
        pass

    def process_prompt_response(self):
        pass
