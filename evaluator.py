from interpreter import *

def find_next_lambda(tokens: Parser):
    while tokens.peek() != TokenTypes.LAMBDA:
        tokens.advance()

def parse_arguments(tokens: Parser):
    args = []
    
    while tokens.peek() == TokenTypes.ARGUMENT:
        arg_name = tokens.consume().value
        if arg_name == None: raise ParseError("Unnamed argument somewhere!!! oopsie!!")
        args += [arg_name]
    
    return tuple(args)

def parse_expression(tokens: Parser):
    expression_tokens = []
    
    while tokens.peek() not in [TokenTypes.LAMBDA, TokenTypes.ARGUMENT, None]:
        expression_tokens += [tokens.consume()]
    
    return Expression(expression_tokens)

def parse_lambda(tokens: Parser):
    arguments = parse_arguments(tokens)
    expression = parse_expression(tokens)

    return Lambda(arguments, expression)

def parse_tokens(tokens: Parser):
    parsed_lambdas = []
    
    while len(tokens) > 0:
        find_next_lambda(tokens) # Remove all leading non-LAMBDA tokens
        tokens.consume()         # Remove leading LAMBDA token
        parsed_lambdas += [parse_lambda(tokens)]
    
    return parsed_lambdas

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

tokens = Parser([])

for line in token_string.splitlines()[1:]:
    token_def = line.split()

    if len(token_def) > 1:
        value = token_def[1]
    else:
        value = None
    
    tokens.token_list += [Token(TokenTypes[token_def[0]], value)]

print(parse_tokens(tokens))