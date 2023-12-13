import tokenize
from io import BytesIO

# Function for lexical analysis
def lexical_analysis(expression):
    tokens = []
    for tok in tokenize.tokenize(BytesIO(expression.encode('utf-8')).readline):
        tokens.append((tokenize.tok_name[tok.type], tok.string))
    return tokens

# Function for parser analysis
def parser_analysis(tokens):
    ast = {'operator': None, 'left': None, 'right': None}
    current_node = ast

    for token_type, token_value in tokens:
        if token_type == 'NAME':
            current_node['left'] = token_value
        elif token_type == 'OP':
            if token_value == '=':
                current_node['operator'] = token_value
                current_node['right'] = {'operator': None, 'left': None, 'right': None}
                current_node = current_node['right']
            elif token_value in {'+', '-', '*', '/'}:
                current_node['operator'] = token_value
                current_node['right'] = {'operator': None, 'left': None, 'right': None}
                current_node = current_node['right']
            elif token_value == '**':
                current_node['operator'] = token_value
                current_node['right'] = {'operator': None, 'left': None, 'right': None}
                current_node = current_node['right']
        elif token_type == 'NUMBER':
            current_node['left'] = token_value

    return ast

#Function for evaluation
def evaluate(input):
    #Process the input
    def process_variable(variable):
        # Remove whitespaces and split the variable by '='
        parts = variable.replace(" ", "").split('=')

        # Ensure there is an equal sign and at least two parts
        if len(parts) >= 2:
            # Return the part after the equal sign
            return parts[1]
        else:
            # If no equal sign is found or only one part is present, return the original variable
            return variable
    input = process_variable(input)
    
    # Lexer
    def tokenize_expression(expression):
        tokens = []
        current_token = ""

        for char in expression:
            if char.isspace():
                continue
            elif char.isdigit() or char == ".":
                current_token += char
            else:
                if current_token:
                    tokens.append(float(current_token))
                    current_token = ""
                tokens.append(char)

        if current_token:
            tokens.append(float(current_token))

        return tokens

    # Parser
    def parse_tokens(tokens):
        index = 0

        def parse_expression():
            nonlocal index
            left_operand = parse_term()

            while index < len(tokens) and tokens[index] in ["+", "-"]:
                operator = tokens[index]
                index += 1
                right_operand = parse_term()

                if operator == "+":
                    left_operand += right_operand
                else:
                    left_operand -= right_operand

            return left_operand

        def parse_term():
            nonlocal index
            left_operand = parse_factor()

            while index < len(tokens) and tokens[index] in ["*", "/"]:
                operator = tokens[index]
                index += 1
                right_operand = parse_factor()

                if operator == "*":
                    left_operand *= right_operand
                else:
                    left_operand /= right_operand

            return left_operand

        def parse_factor():
            nonlocal index
            if tokens[index] == "(":
                index += 1
                result = parse_expression()
                index += 1
                return result
            else:
                result = tokens[index]
                index += 1
                return result

        return parse_expression()


    # Evaluator
    def evaluate_math_expression(expression):
        tokens = tokenize_expression(expression)
        result = parse_tokens(tokens)
        return result


    # ESvaluation
    answer = evaluate_math_expression(input)
    print("\nFinal Result of ({0}) is".format(input), answer)
    return ""







# Expressions
x = "x = 4 / 5 * 8"
y = "y = 2.0 + 5 * 2"

print("Lexer Analysis, Parsing, and Evaluation of x\n")
# Lexical Analysis of x
tokens = lexical_analysis(x) #for x ma'am
print("Lexical Analysis Result of ({0}):".format(x))
print(tokens)
# Parser Analysis of x
ast = parser_analysis(tokens)
print("\nParser Analysis Result (Abstract Syntax Tree):")
print(ast)
# Evaluation of x
print(evaluate(x),"\n\n")

print("Lexer Analysis, Parsing, and Evaluation of y\n")
# Lexical Analysis of y
tokens = lexical_analysis(y) #for y naman po
print("Lexical Analysis Result of ({0}):".format(y))
print(tokens)
# Parser Analysis of y
ast = parser_analysis(tokens)
print("\nParser Analysis Result (Abstract Syntax Tree):")
print(ast)
# Evaluation of y
print(evaluate(y))
