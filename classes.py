from tokens import *

class EvaluationError(Exception):
    pass

@dataclass
class Expression:
    tokens: list[Token]

    def evaluate(self):
        pass

@dataclass
class Lambda:
    vars: list[str]
    expression: Expression

    def evaluate(self, *args):
        var_to_arg_dict = dict(zip(self.vars, args))