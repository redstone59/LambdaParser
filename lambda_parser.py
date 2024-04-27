from expressions import *
from astprinter import AstPrinter

"""
    lambda -> LAMBDA (ARGUMENT)* expression
expression -> equality
  equality -> comparison ( (EQUAL | NOT_EQUAL) comparison )*
comparison -> term ( (GREATER | GREATER_EQUAL | LESS_EQUAL | LESS) term )*
      term -> factor ( (PLUS | MINUS) factor )*
    factor -> unary ( (STAR | SLASH) unary )*
     unary -> ( NOT | MINUS ) unary
     unary -> primary
      call -> primary ( LEFT_PAREN arguments? RIGHT_PAREN )*
   primary -> number | BOOLEAN | LEFT_PAREN expression RIGHT_PAREN

arguments -> ( expression )?
    number -> LITERAL | VARIABLE

lambda x: 2 * lambda: x + 5
LAMBDA ARGUMENT x LAMBDA VARIABLE x PLUS LITERAL 5 STAR LITERAL 2
                         +-----------------------+ term (NUMBER PLUS NUMBER)
                  +------------------------------+ lambda (LAMBDA term)
                  +---------------------------------------------+ factor (NUMBER PLUS lambda)
+---------------------------------------------------------------+ lambda (LAMBDA ARGUMENT factor)
"""

class ParseError(Exception):
    pass 

@dataclass
class Parser:
    token_list: list[Token]
    index: int = 0

    # The below deals with working with token_list.

    def is_at_end(self):
        return self.index >= len(self)

    def advance(self):
        self.index += 1

    def check(self, *token_types: TokenTypes):
        return self.peek() in token_types

    def consume(self, token_type: TokenTypes, error_message: str = ""):
        if self.peek() != token_type: raise ParseError(error_message)
        self.index += 1
        return self.token_list[self.index - 1]

    def peek(self):
        if self.is_at_end(): return None
        return self.token_list[self.index].type

    def previous(self):
        return self.token_list[self.index - 1]

    def match(self, *token_types: TokenTypes):
        if self.check(*token_types):
            self.advance()
            return True
        
        return False
    
    # The below parses based on the grammar above.
    
    def expression(self):
        return self.equality()
    
    def equality(self):
        expression = self.comparison()
        
        while self.match(TokenTypes.EQUAL, TokenTypes.NOT_EQUAL):
            operator = self.previous()
            right = self.comparison()
            
            expression = Binary(expression, operator, right)
        
        return expression
    
    def comparison(self):
        expression = self.term()
        
        while self.match(TokenTypes.GREATER, TokenTypes.GREATER_EQUAL, TokenTypes.LESS_EQUAL, TokenTypes.LESS):
            operator = self.previous()
            right = self.term()
            
            expression = Binary(expression, operator, right)
        
        return expression
    
    def term(self):
        expression = self.factor()
        
        while self.match(TokenTypes.PLUS, TokenTypes.MINUS):
            operator = self.previous()
            right = self.factor()
            
            expression = Binary(expression, operator, right)
        
        return expression
    
    def factor(self):
        expression = self.unary()
        
        while self.match(TokenTypes.STAR, TokenTypes.SLASH):
            operator = self.previous()
            right = self.unary()
            
            expression = Binary(expression, operator, right)
        
        return expression
    
    def unary(self):
        if self.match(TokenTypes.NOT, TokenTypes.MINUS):
            operator = self.previous()
            right = self.unary()
            
            return Unary(operator, right)
        
        return self.primary()
    
    def primary(self):
        if self.match(TokenTypes.TRUE): return Literal(True)
        if self.match(TokenTypes.FALSE): return Literal(False)
        
        if self.match(TokenTypes.LITERAL): return Literal(self.previous().value)
        if self.match(TokenTypes.VARIABLE): return Variable(self.previous().name, self.previous().value)
        if self.match(TokenTypes.BOOLEAN): return Literal(self.previous().value)
        
        if self.match(TokenTypes.LEFT_PAREN):
            expression = self.expression()
            self.consume(TokenTypes.RIGHT_PAREN, "Unclosed bracket for expression.")
            return Grouping(expression)
    
    # Parse
    
    def parse(self):
        #try:
            return self.equality()
        #except ParseError:
        #    return None
    
    # Dunder methods
    
    def __len__(self):
        return len(self.token_list)