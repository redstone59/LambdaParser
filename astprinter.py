from expressions import *

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
        return f"(VAR {variable.name}, {variable.value})"
    
    def visit_unary(self, unary):
        return self.parenthesise(unary.operator.type.name, unary.right)