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