from dataclasses import dataclass
from enum import Enum

class TokenTypes(Enum): # vscode will kill me if i don't have this so
    pass

TokenTypes = Enum("TokenTypes", [
                   "LEFT_PAREN", "RIGHT_PAREN",                      # Groupings
                   "PLUS", "MINUS", "STAR", "SLASH", "PERCENT",      # Operators
                   "EQUAL", "NOT_EQUAL",                             # Equality
                   "GREATER", "GREATER_EQUAL", "LESS", "LESS_EQUAL", # Comparisons
                   "VARIABLE", "LITERAL", "BOOLEAN",                 # Number types
                   "LAMBDA", "ARGUMENT",                             # Defining lambdas
                   "IF", "ELSE",                                     # Conditionals
                   "AND", "OR", "NOT"                                # Logical operators
                 ]
                )

@dataclass
class Token:
    type: TokenTypes
    value: int | bool | str | None = None

    def __repr__(self):
        return f"Token({self.type.name}, {self.value})"

@dataclass
class TokenList:
    token_list: list[Token]
    index: int = 0

    def advance(self):
        if len(self.token_list) == 0: return
        self.token_list.pop(0)

    def check(self, *token_types: TokenTypes):
        return self.peek(self.token_list) in token_types

    def consume(self):
        if len(self.token_list) == 0: return None
        return self.token_list.pop(0)

    def peek(self):
        if len(self.token_list) == 0: return None
        return self.token_list[0].type

    def match(self, *token_types: TokenTypes):
        return self.consume(self.token_list) in token_types
    
    def __len__(self):
        return len(self.token_list)