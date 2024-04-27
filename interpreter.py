from lambda_parser import *

class EvaluationError(Exception):
    pass

@dataclass
class Interpreter(ExpressionVisitor):
    def evaluate(self, expression: Expression):
        return expression.accept(self)
    
    def check_for_var(self, expression):
        # If a variable with no value is passed in, parsing it will return an Expression
        return type(expression) == Variable
    
    def visit_binary(self, binary: Binary):
        left = binary.left.accept(self)
        right = binary.right.accept(self)
        
        if self.check_for_var(left) or self.check_for_var(right):
            return Binary(left, binary.operator, right)
        
        match binary.operator.type:
            # Arithmetic operations
            case TokenTypes.PLUS:
                return Literal(left + right)
            case TokenTypes.MINUS:
                return Literal(left - right)
            case TokenTypes.STAR:
                return Literal(left * right)
            case TokenTypes.SLASH:
                return Literal(left / right)
            case TokenTypes.PERCENT:
                return Literal(left % right)
            # Comparisons
            case TokenTypes.GREATER:
                return Literal(left > right)
            case TokenTypes.GREATER_EQUAL:
                return Literal(left >= right)
            case TokenTypes.LESS_EQUAL:
                return Literal(left <= right)
            case TokenTypes.LESS:
                return Literal(left < right)
            # Equality
            case TokenTypes.EQUAL:
                return Literal(left == right)
            case TokenTypes.NOT_EQUAL:
                return Literal(left != right)
    
    def visit_grouping(self, grouping: Grouping):
        return grouping.expression.accept(self)
    
    def visit_literal(self, literal: Literal):
        return literal.value
    
    def visit_variable(self, variable: Variable):
        if variable.value == None: return variable
        return variable.value
    
    def visit_unary(self, unary: Unary):
        right = unary.right.accept(self)
        
        if self.check_for_var(right):
            return unary
        
        match unary.operator.type:
            case TokenTypes.NOT:
                # Everything but a literal with value False is truthy.
                return Literal(type(right) == bool and right == False)
            case TokenTypes.MINUS:
                return Literal(-right)


"""
@dataclass
class Interpreter:
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
        """