from tokens import *

class ExpressionVisitor:
    def visit_binary(self, binary):
        pass
    
    def visit_grouping(self, grouping):
        pass
    
    def visit_literal(self, literal):
        pass
    
    def visit_variable(self, variable):
        pass
    
    def visit_unary(self, unary):
        pass


class AstPrinter(ExpressionVisitor):
    def print(self, expression):
        return expression.accept(self)
    
    def parenthesise(self, name, *expressions):
        expressions = list(expressions)
        result = "(" + name
        
        for expression in expressions:
            result += " "
            result += expression.accept(self)
        
        result += ")"
        return result
    
    def visit_binary(self, binary):
        return self.parenthesise(binary.operator.type.name, binary.left, binary.right)
    
    def visit_grouping(self, grouping):
        return self.parenthesise("GROUP", grouping.expression)
    
    def visit_literal(self, literal):
        return str(literal.value)
    
    def visit_variable(self, variable):
        return self.parenthesise("var", variable.name, variable.value)
    
    def visit_unary(self, unary):
        return self.parenthesise(unary.operator.type.name, unary.right)

class Expression:
    def accept(self, visitor: ExpressionVisitor):
        raise NotImplementedError("accept() not implemented for class")

@dataclass
class Binary(Expression):
    left: Expression
    operator: Token
    right: Expression
    
    def accept(self, visitor: ExpressionVisitor):
        return visitor.visit_binary(self)

@dataclass
class Grouping(Expression):
    expression: Expression
    
    def accept(self, visitor: ExpressionVisitor):
        return visitor.visit_grouping(self)

@dataclass
class Literal(Expression):
    value: int | bool | str
    
    def accept(self, visitor: ExpressionVisitor):
        return visitor.visit_literal(self)

@dataclass
class Variable(Expression):
    name: str
    value: int | bool | None = None
    
    def accept(self, visitor: ExpressionVisitor):
        return visitor.visit_variable(self)

@dataclass 
class Unary(Expression):
    operator: Token
    right: Expression
    
    def accept(self, visitor: ExpressionVisitor):
        return visitor.visit_unary(self)

expression = Binary(
    Unary(
        Token(TokenTypes.MINUS),
        Literal(123)
    ),
    Token(TokenTypes.STAR),
    Grouping(
        Literal(456)
    )
)

print(AstPrinter().print(expression))