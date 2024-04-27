from interpreter import *

token_string = """
VARIABLE x
PLUS
LITERAL 3
STAR
VARIABLE y 12
"""

tokens = Parser([])

for line in token_string.splitlines()[1:]:
    token_def = line.split()

    if len(token_def) > 1:
        value = token_def[1]
    else:
        value = None
    
    name = None
    
    match token_def[0]:
        case "LITERAL":
            try:
                value = int(value)
            except:
                value = float(value)
        case "BOOLEAN":
            if value.lower() == "false":
                value = False
            else:
                value = True
        case "VARIABLE":
            name = token_def[1]
            if len(token_def) == 3:
                value = token_def[2]
                try:
                    value = int(value)
                except:
                    value = float(value)
            else:
                value = None
    
    tokens.token_list += [Token(TokenTypes[token_def[0]], value, name = name)]


expression = tokens.parse()
print(AstPrinter().print(expression))
value = Interpreter().evaluate(expression)
if type(value) not in [int, float, bool]:
    print(AstPrinter().print(value))
else:
    print(value)