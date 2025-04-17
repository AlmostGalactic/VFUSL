'''
VFUSL stands for Very Full Stack Language (Dont ask what the U is for).
It is where every code piece is a stack operation.
'''

class Environment:
    def __init__(self, parent=None):
        self.parent = parent
        self.functions = {}
    
    def create_func(self, name, code):
        if name in self.functions or (self.parent and name in self.parent.functions):
            raise ValueError(f"Function '{name}' already exists")
        self.functions[name] = code
    
    def get_func(self, name):
        if name in self.functions:
            return self.functions[name]
        elif self.parent:
            return self.parent.get_func(name)
        else:
            raise ValueError(f"Function '{name}' not found")


class Interpreter:
    def __init__(self):
        self.stack = []
        self.env = Environment()
        self.builtins = {
            'print': self._print,
            ':': self._dup,
            '+': self._add,
            '-': self._sub,
            '*': self._mul,
            '/': self._div,
            '%': self._mod,
            '==': self._eq,
            '!=': self._ne,
            '<': self._lt,
            '<=': self._le,
            '>': self._gt,
            '>=': self._ge,
            '<--?': self._if,
            "exec": self._exec,
            "create": self._func,
            "@in": self._input,
            "@ord": self._ord,
            "@chr": self._chr,
            "write": self._write,
            "whl": self._while
        }

    def _print(self):
        if not self.stack:
            raise ValueError("Stack is empty")
        print(self.stack.pop())

    def _dup(self):
        if not self.stack:
            raise ValueError("Stack is empty")
        self.stack.append(self.stack[-1])

    def _add(self):
        a, b = self.stack.pop(), self.stack.pop()
        self.stack.append(b + a)

    def _sub(self):
        a, b = self.stack.pop(), self.stack.pop()
        self.stack.append(b - a)

    def _mul(self):
        a, b = self.stack.pop(), self.stack.pop()
        self.stack.append(b * a)

    def _div(self):
        a, b = self.stack.pop(), self.stack.pop()
        if a == 0:
            raise ZeroDivisionError("Division by zero")
        self.stack.append(b / a)

    def _mod(self):
        a, b = self.stack.pop(), self.stack.pop()
        if a == 0:
            raise ZeroDivisionError("Modulo by zero")
        self.stack.append(b % a)

    def _eq(self):
        a, b = self.stack.pop(), self.stack.pop()
        self.stack.append(b == a)

    def _ne(self):
        a, b = self.stack.pop(), self.stack.pop()
        self.stack.append(b != a)

    def _lt(self):
        a, b = self.stack.pop(), self.stack.pop()
        self.stack.append(b < a)

    def _le(self):
        a, b = self.stack.pop(), self.stack.pop()
        self.stack.append(b <= a)

    def _gt(self):
        a, b = self.stack.pop(), self.stack.pop()
        self.stack.append(b > a)

    def _ge(self):
        a, b = self.stack.pop(), self.stack.pop()
        self.stack.append(b >= a)

    def _if(self):
        if len(self.stack) < 3:
            raise ValueError("Not enough values on stack for 'if'")
        
        else_ = self.stack.pop()
        then_ = self.stack.pop()
        cond = self.stack.pop()

        if cond:
            self.run_tokens(then_)
        else:
            self.run_tokens(else_)


    def _exec(self):
        code = self.stack.pop()
        if isinstance(code, str):
            code = self.env.get_func(code)
        if not isinstance(code, list):
            raise ValueError("exec expects a code block or function name")
        self.run_tokens(code, Environment(self.env))

    def _func(self):
        name = self.stack.pop()
        code = self.stack.pop()
        if not isinstance(name, str):
            raise ValueError("Function name must be a string")
        self.env.create_func(name, code)

    def _input(self):
        take = input()
        try:
            inp = int(take)
        except ValueError:
            try:
                inp = float(take)
            except ValueError:
                pass
        self.stack.append(inp)

    def _chr(self):
        value = int(self.stack.pop())
        self.stack.append(chr(value))

    def _ord(self):
        value = self.stack.pop()
        if not isinstance(value, str) or len(value) != 1:
            raise ValueError("Expected single character string")
        self.stack.append(ord(value))

    def _write(self):
        print(self.stack.pop(), end='')

    def _while(self):
        if len(self.stack) < 2:
            raise ValueError("Not enough values on stack for 'while'")
        
        body = self.stack.pop()
        condition = self.stack.pop()

        if not isinstance(condition, list) or not isinstance(body, list):
            raise ValueError("'while' expects two code blocks")

        while True:
            self.run_tokens(condition)
            if not self.stack:
                raise ValueError("Condition block did not leave a value on the stack")
            result = self.stack.pop()
            if not result:
                break
            self.run_tokens(body)


    def tokenize(self, code):
        tokens = []
        i = 0
        while i < len(code):
            char = code[i]

            if char.isspace():
                i += 1
                continue
            
            if char == "#":
                break

            # Code block [ ... ]
            elif char == '[':
                depth = 1
                i += 1
                block = ''
                while i < len(code) and depth > 0:
                    if code[i] == '[':
                        depth += 1
                    elif code[i] == ']':
                        depth -= 1
                        if depth == 0:
                            i += 1
                            break
                    block += code[i]
                    i += 1
                tokens.append(self.tokenize(block.strip()))
            
            # String literal |...|
            elif char == '|':
                i += 1
                string_val = ''
                while i < len(code) and code[i] != '|':
                    string_val += code[i]
                    i += 1
                if i == len(code):
                    raise SyntaxError("Unterminated string literal")
                i += 1  # Skip ending |
                tokens.append(string_val)

            # Number or word
            else:
                token = ''
                while i < len(code) and not code[i].isspace() and code[i] not in '[]|':
                    token += code[i]
                    i += 1
                try:
                    token = int(token)
                except ValueError:
                    try:
                        token = float(token)
                    except ValueError:
                        pass
                tokens.append(token)
        return tokens

    def parse_tokens(self, tokens):
        if isinstance(tokens, list):
            return [self.parse_tokens(t) for t in tokens]
        return tokens

    def run_tokens(self, tokens, parent_env=None):
        env = parent_env or self.env
        for token in tokens:
            val = self.parse_tokens(token)
            self.stack.append(val)

            if isinstance(val, str):
                if val in self.builtins:
                    self.stack.pop()
                    self.builtins[val]()
                elif val in env.functions:
                    self.stack.pop()
                    self.stack.append(env.get_func(val))

    def execute(self, code):
        code = code.replace("\n", " ")
        tokens = self.tokenize(code)
        self.run_tokens(tokens)
        return self.stack
