import lexer

class VarDecl:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        
    def __repr__(self):
        return f"VarDecl<name={self.name} value={self.value}>"

class FuncCall:
    def __init__(self, name, args):
        self.name = name
        self.args = args
        
    def __repr__(self):
        return f"FuncCall<name={self.name} args={self.args}>"

class ParserError(Exception):
    pass

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        
    def peek(self, offset=0):
        if self.pos + offset < len(self.tokens):
            return self.tokens[self.pos + offset]
        return None
    
    def advance(self):
        self.pos += 1
        
    def match(self, *types):
        token = self.peek()
        if token and token.type in types:
            self.advance()
            return token
        return None
    
    def expect(self, type_):
        token = self.match(type_)
        if not token:
            raise ParserError(f"Expected {type_} at position {self.pos}")
        return token
    
    def parse(self):
        ast = []
        while self.peek():
            stmt = self.parse_statement()
            if stmt:
                ast.append(stmt)
        return ast
    
    def parse_statement(self):
        if self.peek().type == "LET":
            return self.parse_var_decl()
        elif self.peek().type == "IDENT":
            return self.parse_func_call()
        else:
            raise ParserError(f"Unknown statement at {self.peek()}")
    
    def parse_var_decl(self):
        self.expect("LET")
        name = self.expect("IDENT").value
        self.expect("EQUAL")
        value = self.parse_expression()
        self.expect("SEMICOLON")
        return VarDecl(name, value)
    
    def parse_func_call(self):
        name = self.expect("IDENT").value
        self.expect("LPAREN")
        args = []
        if self.peek().type != "RPAREN":
            args.append(self.parse_expression())
            while self.match("COMMA"):
                args.append(self.parse_expression())
        self.expect("RPAREN")
        self.expect("SEMICOLON")
        return FuncCall(name, args)
    
    def parse_expression(self):
        token = self.peek()
        if token.type == "NUMBER":
            self.advance()
            return int(token.value) if '.' not in token.value else float(token.value)
        elif token.type == "STRING":
            self.advance()
            return token.value[1:-1]
        elif token.type == "IDENT":
            self.advance()
            return token.value
        else:
            raise ParserError(f"Invalid expression at {token}")
        
tokens = lexer.example()
parser = Parser(tokens)
ast = parser.parse()

for node in ast:
    print(node)