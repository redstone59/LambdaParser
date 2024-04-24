from classes import *

class ParseError(Exception):
    pass 

def advance(token_list: list[Token]):
    token_list.pop(0)

def consume(token_list: list[Token]):
    return token_list.pop(0)

def find_next_lambda(token_list: list[Token]):
    while peek(token_list) != TokenTypes.LAMBDA:
        advance(token_list)

def peek(token_list: list[Token]):
    return token_list[0].type

def parse_arguments(token_list: list[Token]):
    args = []
    while peek(token_list) == TokenTypes.ARGUMENT:
        arg_name = consume(token_list).value
        if arg_name == None: raise ParseError("Unnamed argument somewhere!!! oopsie!!")
        args += [arg_name]
    
    return tuple(args)

def parse_expression(token_list: list[Token]):
    expression_tokens = []
    while peek(token_list) not in [TokenTypes.LAMBDA, TokenTypes.ARGUMENT]:
        expression_tokens += [consume(token_list)]
    
    return Expression(expression_tokens)

def parse_lambda(token_list: list[Token]):
    arguments = parse_arguments(token_list)
    expression = parse_expression(token_list)

    return Lambda(arguments, expression)

def parse_tokens(token_list: list[Token]):
    while len(token_list) > 0:
        find_next_lambda(token_list)
        parse_lambda(token_list)
    
    print("Completed parsing") 

token_string = """
LAMBDA
ARGUMENT x
ARGUMENT y
VARIABLE x
STAR
VARIABLE x
PLUS
VARIABLE y
""" # the above should be equal to `lambda x, y: x * x + y`

token_list = []

for line in token_string.splitlines()[1:]:
    token_def = line.split()

    if len(token_def) > 1:
        value = token_def[1]
    else:
        value = None
    
    token_list += [Token(TokenTypes[token_def[0]], value)]

parse_tokens(token_list)