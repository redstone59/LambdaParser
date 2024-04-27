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
                   "TRUE", "FALSE",                                  # Boolean values
                   "LAMBDA", "ARGUMENT",                             # Defining lambdas
                   "IF", "ELSE",                                     # Conditionals
                   "AND", "OR", "NOT",                               # Logical operators
                   "COMMA",                                          # Calling
                 ]
                )

@dataclass
class Token:
    type: TokenTypes
    value: int | float | bool | str | None = None
    name: str | None = None

    def __repr__(self):
        return f"Token({self.type.name}, {self.value})"