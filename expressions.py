
from re import compile, Pattern
from typing import List, Tuple

import math

class TokenType:
    NUMBER = 1
    ADD    = 2
    SUB    = 3
    USUB   = 33
    MUL    = 4
    DIV    = 5
    EXP    = 6

    LPAREN = 9
    RPAREN = 10
    
    VARIABLE = 11
    FUNCTION = 12
    COMMA = 13

    NONE = 99

    PRECENDENCE = {
        2: 1,
        3: 1,
        4: 2,
        5: 2,
        6: 3,

        9: 3,
        10: 3,
        12: 0,

        33: 9
    }

    FUNCTIONS = {
        'sin': (1, lambda args: math.sin(args[0])),
        'cos': (1, lambda args: math.cos(args[0])),
        'tan': (1, lambda args: math.tan(args[0])),
        'asin': (1, lambda args: math.asin(args[0])),
        'acos': (1, lambda args: math.acos(args[0])),
        'atan': (1, lambda args: math.atan(args[0])),
        'asinh': (1, lambda args: math.asinh(args[0])),
        'acosh': (1, lambda args: math.acosh(args[0])),
        'atanh': (1, lambda args: math.atanh(args[0])),
        'atan2': (2, lambda args: math.atan2(args[0], args[1])),
        'ceil': (1, lambda args: math.ceil(args[0])),
        'floor': (1, lambda args: math.floor(args[0])),
        'sqrt': (1, lambda args: math.sqrt(args[0])),
        'sign': (1, lambda args: -1 if args[0] < 0 else (0 if args[0] == 0 else 1)),
        'pow': (2, lambda args: pow(*args)),
        'max': (2, lambda args: max(*args)),
        'min': (2, lambda args: min(*args)),
        'deg': (1, lambda args: math.degrees(*args)),
        'rad': (1, lambda args: math.radians(*args)),
    }

    OPERANDS = {
        2: lambda a, b: b + a,
        3: lambda a, b: b - a,
        4: lambda a, b: b * a,
        5: lambda a, b: b / a,
        6: lambda a, b: pow(b, a),
        33: lambda a, b: -a
    }

    @staticmethod
    def get_precedence(type):
        return TokenType.PRECENDENCE[type] or 0

    @staticmethod
    def is_left_associative(type):
        return type != TokenType.EXP and type != TokenType.USUB

    @staticmethod
    def perform_operand(type, a, b):
        return TokenType.OPERANDS[type](a, b)

    @staticmethod
    def is_number(type):
        return type == TokenType.NUMBER

    @staticmethod
    def is_operator(type):
        return type >= TokenType.ADD and type <= TokenType.EXP or type == TokenType.USUB

class Token:
    def __init__(self, type, value: str) -> None:
        self.type = type
        self.value = value
    
    def clone(self):
        return Token(self.type, self.value)
    
    def __repr__(self):
        name = self.type
        for attr in dir(TokenType):
            if getattr(TokenType, attr) == self.type:
                name = attr
                break
        return f'Token({name} -> {self.value})'

TOKENS: List[Tuple[int, Pattern]] = [
    (TokenType.NONE, compile(r'^\s+')),
    (TokenType.COMMA, compile(r'^\,')),
    (TokenType.USUB, compile(r'^\-\(')),
    (TokenType.NUMBER, compile(r'^-?\d+(?:\.\d+)?')),
    (TokenType.ADD, compile(r'^\+')),
    (TokenType.SUB,  compile(r'^\-')),
    (TokenType.MUL, compile(r'^\*')),
    (TokenType.DIV, compile(r'^\/')),
    (TokenType.EXP, compile(r'^\^')),
    (TokenType.LPAREN, compile(r'^\(')),
    (TokenType.RPAREN, compile(r'^\)')),
    (TokenType.FUNCTION, compile(r'^[a-zA-Z]+\(')),
    (TokenType.VARIABLE, compile(r'^[a-zA-Z]+')),
]

def tokenize(expression: str):
    tokens = []

    while len(expression) > 0:
        found = False
        for (type, pattern) in TOKENS:
            match = pattern.match(expression)
            if not match:
                continue
            expression = expression[match.span(0)[1]:]
            found = True
            if type == TokenType.NONE:
                break
            if type == TokenType.USUB:
                if len(tokens) == 0 or tokens[-1].type == TokenType.LPAREN:
                    expression = '(' + expression
                else:
                    continue
            if type == TokenType.SUB:
                if len(tokens) == 0:
                    type = TokenType.USUB
            tokens.append(Token(type, match.group(0)))
            if type == TokenType.USUB:
                tokens[-1].value = tokens[-1].value[0]
            if type == TokenType.FUNCTION:
                tokens[-1].value = tokens[-1].value.rstrip('(')
                tokens.append(Token(TokenType.LPAREN, '('))
            elif type == TokenType.NUMBER:
                tokens[-1].value = float(tokens[-1].value) if '.' in tokens[-1].value else int(tokens[-1].value)
                if tokens[-1].value < 0:
                    if len(tokens) > 1 and not TokenType.is_operator(tokens[-2].type):
                        tokens.insert(-1, Token(TokenType.ADD, '+'))
            break
        if not found:
            raise ValueError("Unexpected token " + expression[0:]) # invalid token
    
    return tokens

class Stack:
    def __init__(self):
        self.list = []
    
    def push(self, x: Token) -> None:
        self.list.append(x)
    
    def pop(self) -> Token:
        return self.list.pop()

    def peek(self) -> Token:
        return self.list[-1]

    def __len__(self) -> int:
        return len(self.list)

def shunting_yard(tokens: List[Token]):
    output = []
    stack = Stack()
    while len(tokens) > 0:
        #print(' '.join(list(map(lambda x: x.value, stack.list[::-1]))))
        token = tokens.pop(0)

        if TokenType.is_number(token.type) or token.type == TokenType.VARIABLE:
            output.append(token)
        elif token.type == TokenType.FUNCTION:
            stack.push(token)
        elif TokenType.is_operator(token.type):
            while len(stack) > 0 and stack.peek().type != TokenType.LPAREN and \
                ((TokenType.get_precedence(stack.peek().type) > TokenType.get_precedence(token.type)) \
                or (TokenType.get_precedence(stack.peek().type) == TokenType.get_precedence(token.type) \
                and TokenType.is_left_associative(token.type))):
                output.append(stack.pop())
            stack.push(token)
        elif token.type == TokenType.COMMA:
            continue
        elif token.type == TokenType.LPAREN:
            stack.push(token)
        elif token.type == TokenType.RPAREN:
            if len(stack) == 0:
                raise ValueError('Unexpected right parenthesis')
            while stack.peek().type != TokenType.LPAREN:
                output.append(stack.pop())
                if len(stack) == 0:
                    raise ValueError('Unexpected right parenthesis')
            stack.pop()
            if stack.peek().type == TokenType.FUNCTION:
                output.append(stack.pop())

    for i in range(len(stack)):
        output.append(stack.pop())

    return output

def calculate(postfix: List[Token], variables: dict, functions: dict):
    stack = Stack()

    # variable passover
    for token in postfix:
        if token.type == TokenType.VARIABLE:
            if token.value not in variables:
                raise ValueError('Invalid variable ' + token.value)
            token.value = variables.get(token.value)
            token.type = TokenType.NUMBER

    # evaluate
    for token in postfix:
        #print(' '.join(list(map(lambda x: str(x), stack.list))))
        if TokenType.is_number(token.type):
            stack.push(token.value)
        else:
            if token.type == TokenType.FUNCTION:
                a = TokenType.FUNCTIONS.get(token.value, functions.get(token.value))
                if a == None:
                    raise ValueError('Invalid function', token.value)
                value = a[1]([stack.pop() for _ in range(a[0])])
                stack.push(value)
            elif token.type == TokenType.USUB:
                stack.push(TokenType.perform_operand(token.type, stack.pop(), None))
            else:
                stack.push(TokenType.perform_operand(token.type, stack.pop(), stack.pop()))
    
    if len(stack) > 1:
        raise ValueError('Too many tokens after evaluation! Missing operator?')

    return stack.pop()

class Expression:
    def __init__(self, expression: str):
        self.expression = expression
        self.parse()

    def parse(self) -> None:
        tokens = tokenize(self.expression)
        self.postfix = shunting_yard(tokens)

    def evaluate(self, variables: dict = {}, functions: dict = {}):
        variables['pi'] = math.pi
        variables['tau'] = math.tau
        return calculate([t.clone() for t in self.postfix], variables, functions)

if __name__ == '__main__':
    from sys import argv
    print('  INPUT ->', ' '.join(argv[1:]))
    tokens = tokenize(' '.join(argv[1:]))
    print('  INFIX ->', ' '.join(list(map(lambda x: str(x.value), tokens))))
    print(tokens)
    postfix = shunting_yard(tokens)
    print('POSTFIX ->', ' '.join(list(map(lambda x: str(x.value), postfix))))
    answer = calculate(postfix, {
        'pi': math.pi
    })
    print(' ANSWER ->', round(answer, 5))