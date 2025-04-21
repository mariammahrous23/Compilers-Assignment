import string


def tokenize(regex):
    tokens = []
    i = 0
    while i < len(regex):
        char = regex[i]
        
        if char == '[':
            j = i + 1
            while j < len(regex) and regex[j] != ']':
                j += 1
            if j == len(regex):
                raise ValueError("Unclosed character class '['")
            bracket_token = regex[i:j+1]  
            expanded = expand_lists(bracket_token)  
            tokens.extend(tokenize(expanded))  # recursively tokenize the expanded characters
            i = j + 1
        elif char in {'(', ')', '*', '+', '?', '|', '.'}:
            tokens.append(char)
            i += 1
        elif char.isalnum():
            tokens.append(char)
            i += 1
        else:
            raise ValueError(f"Unexpected character '{char}' at position {i}")
    
    return tokens

def expand_lists(token):
    allowed_range = set(string.ascii_letters + string.digits)

    if not token.startswith('[') or not token.endswith(']'):
        raise ValueError("Token must be a character class enclosed in brackets")

    content = token[1:-1]
    chars = []
    i = 0
    while i < len(content):
        if i + 2 < len(content) and content[i+1] == '-':  # handle ranges (e.g., a-z)
            start = content[i]
            end = content[i+2]
            if start in allowed_range and end in allowed_range and ord(start) <= ord(end):
                chars.extend([chr(j) for j in range(ord(start), ord(end) + 1)])
                i += 3
            else:
                raise ValueError(f"Invalid range '{start}-{end}' in character class")
        else:  # handle individual characters
            if content[i] in allowed_range:
                chars.append(content[i])
                i += 1
            else:
                raise ValueError(f"Invalid character '{content[i]}' in character class")

    return '(' + '|'.join(sorted(set(chars))) + ')'

def insert_concatenation_operators(tokens):
    result = []
    length = len(tokens)

    for i in range(length - 1):
        current = tokens[i]
        next_char = tokens[i + 1]

        result.append(current)

        # insert a concatenation operator if the current and next tokens should be concatenated
        if (
            (current.isalnum() or current in [')', '*', '+', '?', '.']) and
            (next_char.isalnum() or next_char in ['(', '[', '.'])
        ):
            result.append('#')

    if length > 0:
        result.append(tokens[-1])

    return result

EPSILON = 'ε'

def is_literal(char):
    return char.isalnum() or char == '.' or char == EPSILON

def infix_to_postfix(tokens):
    precedence = {
        '*': 5,
        '+': 4,
        '?': 3,
        '#': 2,
        '|': 1
    }
    
    output = []
    operators = []

    for i in range(1, len(tokens)):
        if tokens[i-1] not in precedence and tokens[i] not in precedence and tokens[i-1] != '(' and tokens[i] != ')':
            tokens.insert(i, '#')

    for token in tokens:
        if token.isalnum() or token == '.':
            output.append(token)
        elif token == '(':
            operators.append(token)
        elif token == ')':
            while operators and operators[-1] != '(':
                output.append(operators.pop())
            if not operators:
                raise ValueError("Mismatched parentheses")
            operators.pop()
        elif token == '*':
            output.append(token)
        elif token in precedence:
            while operators and operators[-1] != '(' and precedence[token] <= precedence.get(operators[-1], 0):
                output.append(operators.pop())
            operators.append(token)

    while operators:
        if operators[-1] == '(' or operators[-1] == ')':
            raise ValueError("Mismatched parentheses")
        output.append(operators.pop())
    
    return output

def preprocessing(regex):
    tokens = tokenize(regex)
    tokens_with_concatenation = insert_concatenation_operators(tokens)
    postfix_tokens = infix_to_postfix(tokens_with_concatenation)
    return postfix_tokens
