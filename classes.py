from tokens import *

class EvaluationError(Exception):
    pass

"""
expression -> equality
equality -> comparison ( (EQUAL | NOT_EQUAL) comparison )*
comparison -> term ( (GREATER | GREATER_EQUAL | LESS_EQUAL | LESS) term )*
term -> factor ( (PLUS | MINUS) factor )*
factor -> unary ( (STAR | SLASH) unary )*
unary -> ( NOT | MINUS ) unary
unary -> primary
primary -> number | BOOLEAN | LEFT_PAREN expession RIGHT_PAREN

number -> LITERAL | VARIABLE
"""

@dataclass
class Expression:
    tokens: list[Token]

    def evaluate(self, tokens: list[Token] | None = None):
        if tokens == None: tokens = self.tokens
    
    def evaluate_with_args(self, **arg_to_var_dict):
        substituted_tokens = self.tokens
        
        for arg in arg_to_var_dict:
            variable_token = Token(TokenTypes.VARIABLE, arg)
            literal_token = Token(TokenTypes.LITERAL, arg_to_var_dict[arg])
            substituted_tokens = self.substitute_token(variable_token, literal_token)
        
        return self.evaluate(substituted_tokens)
    
    def substitute_token(self, find_token: Token, replace_token: Token):
        substituted_tokens = self.tokens
        
        for index in range(len(substituted_tokens)):
            token = substituted_tokens[index]
            if token == find_token:
                substituted_tokens[index] = replace_token
        
        return substituted_tokens

@dataclass
class Lambda:
    args: list[str]
    expression: Expression

    def evaluate(self, *vars):
        arg_to_var_dict = dict(zip(self.args, vars))
        return self.expression.evaluate_with_args(arg_to_var_dict)