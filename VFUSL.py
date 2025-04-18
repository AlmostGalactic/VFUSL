'''
VFUSL stands for Very Full Stack Language (Don't ask what the U is for).
It is where every code piece is a stack operation.
'''

class LiteralString(str):
    pass

class Environment:
    def __init__(self, parent=None):
        self.parent = parent
        self.functions = {}
        self.vars = {}

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

    def set_var(self, name, value):
        if name in self.vars:
            self.vars[name] = value
        elif self.parent:
            self.parent.set_var(name, value)
        else:
            self.vars[name] = value

    def get_var(self, name):
        if name in self.vars:
            return self.vars[name]
        elif self.parent:
            return self.parent.get_var(name)
        else:
            raise ValueError(f"Variable '{name}' not found")


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
            "whl": self._while,
            "define": self._setvar
        }

    def _print(self, env=Environment()):
        if not self.stack:
            raise ValueError("Stack is empty")
        print(self.stack.pop())

    def _dup(self, env=Environment()):
        if not self.stack:
            raise ValueError("Stack is empty")
        self.stack.append(self.stack[-1])

    def _add(self, env=Environment()):
        a, b = self.stack.pop(), self.stack.pop()
        self.stack.append(b + a)

    def _sub(self, env=Environment()):
        a, b = self.stack.pop(), self.stack.pop()
        self.stack.append(b - a)

    def _mul(self, env=Environment()):
        a, b = self.stack.pop(), self.stack.pop()
        self.stack.append(b * a)

    def _div(self, env=Environment()):
        a, b = self.stack.pop(), self.stack.pop()
        if a == 0:
            raise ZeroDivisionError("Division by zero")
        self.stack.append(b / a)

    def _mod(self, env=Environment()):
        a, b = self.stack.pop(), self.stack.pop()
        if a == 0:
            raise ZeroDivisionError("Modulo by zero")
        self.stack.append(b % a)

    def _eq(self, env=Environment()):
        a, b = self.stack.pop(), self.stack.pop()
        self.stack.append(b == a)

    def _ne(self, env=Environment()):
        a, b = self.stack.pop(), self.stack.pop()
        self.stack.append(b != a)

    def _lt(self, env=Environment()):
        a, b = self.stack.pop(), self.stack.pop()
        self.stack.append(b < a)

    def _le(self, env=Environment()):
        a, b = self.stack.pop(), self.stack.pop()
        self.stack.append(b <= a)

    def _gt(self, env=Environment()):
        a, b = self.stack.pop(), self.stack.pop()
        self.stack.append(b > a)

    def _ge(self, env=Environment()):
        a, b = self.stack.pop(), self.stack.pop()
        self.stack.append(b >= a)

    def _if(self, env=Environment()):
        if len(self.stack) < 3:
            raise ValueError("Not enough values on stack for 'if'")
        else_ = self.stack.pop()
        then_ = self.stack.pop()
        cond = self.stack.pop()
        if cond:
            self.run_tokens(then_)
        else:
            self.run_tokens(else_)

    def _exec(self, env=Environment()):
        code = self.stack.pop()
        if isinstance(code, str):
            code = self.env.get_func(code)
        if not isinstance(code, list):
            raise ValueError("exec expects a code block or function name")
        self.run_tokens(code, Environment(self.env))

    def _func(self, env=Environment()):
        name = self.stack.pop()
        code = self.stack.pop()
        if not isinstance(name, str):
            raise ValueError("Function name must be a string")
        env.create_func(name, code)

    def _input(self, env=Environment()):
        take = input()
        try:
            inp = int(take)
        except ValueError:
            try:
                inp = float(take)
            except ValueError:
                inp = take
        self.stack.append(inp)

    def _chr(self, env=Environment()):
        value = int(self.stack.pop())
        self.stack.append(chr(value))

    def _ord(self, env=Environment()):
        value = self.stack.pop()
        if not isinstance(value, str) or len(value) != 1:
            raise ValueError("Expected single character string")
        self.stack.append(ord(value))

    def _write(self, env=Environment()):
        print(self.stack.pop(), end='')

    def _while(self, env=Environment()):
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

    def _setvar(self, env=Environment()):
        if len(self.stack) < 2:
            raise ValueError("Not enough values on stack for 'define'")
        value = self.stack.pop()
        name = self.stack.pop()
        env.set_var(name, value)

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
            elif char == '|':
                i += 1
                string_val = ''
                while i < len(code) and code[i] != '|':
                    string_val += code[i]
                    i += 1
                if i == len(code):
                    raise SyntaxError("Unterminated string literal")
                i += 1
                tokens.append(LiteralString(string_val))
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

    def run_tokens(self, tokens, parent_env=Environment()):
        env = parent_env
        for token in tokens:
            val = self.parse_tokens(token)
            self.stack.append(val)
            if isinstance(val, str) and not isinstance(val, LiteralString):
                if val in self.builtins:
                    self.stack.pop()
                    self.builtins[val](env)
                elif val in env.functions:
                    self.stack.pop()
                    self.stack.append(env.get_func(val))
                elif val in env.vars:
                    self.stack.pop()
                    self.stack.append(env.get_var(val))

    def execute(self, code):
        code = code.replace("\n", " ")
        tokens = self.tokenize(code)
        self.run_tokens(tokens)
        return self.stack
