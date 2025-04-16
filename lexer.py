import re

class Token:
   def __init__(self, type: str, value: str, line: int, col: int):
      self.type = type
      self.value = value
      self.line = line
      self.col = col
      
   def __repr__(self):
      return f"{self.type}({repr(self.value)}) @ {self.line}:{self.col}"
   
TOKEN_SPEC = [
    ( 'NUMBER',        r'-?\d+(\.\d+)?' ),
    ( 'STRING',        r'"(?:\\.|[^"\\])*"' ),
    ( 'LET',           r'\blet\b' ),
    ( 'IDENT',         r'\b[a-zA-Z_][a-zA-Z0-9_]*\b' ),
    ( 'EQUAL',         r'=' ),
    ( 'LPAREN',        r'\(' ),
    ( 'RPAREN',        r'\)' ),
    ( 'COMMA',         r',' ),
    ( 'SEMICOLON',     r';' ),
    ( 'LINE_COMMENT',  r'//.*' ),
    ( 'BLOCK_COMMENT', r'/\*.*?\*/' ),
    ( 'WHITESPACE',    r'[ \t]+' ),
    ( 'NEWLINE',       r'\n' ),
]

TOKEN_REGEX  = "|".join(f'(?P<{name}>{regex})' for name, regex in TOKEN_SPEC)
TOKEN_RE = re.compile(TOKEN_REGEX, re.DOTALL)

def lex(code: str | list):
   if type(code) == list:
      code = "\n".join(code)
      
   line_num = 1
   line_start = 0
   tokens = []
   
   for match in TOKEN_RE.finditer(code):
      kind = match.lastgroup
      value = match.group()
      col = match.start() - line_start
      
      if kind == "NEWLINE":
         line_num += 1
         line_start = match.end()
      elif kind in ["WHITESPACE", "LINE_COMMENT", "BLOCK_COMMENT"]:
         continue
      else:
         tokens.append(Token(kind, value, line_num, col))
         
   return tokens

def example():
   example_code = '''\
   let x1 = 10;
   let block = "minecraft:air";
   fill(x1, y1, z1, x2, y2, z2, block);

   // Line comments are the "//" characters
   /*

      Block comments are /**/ characters

   */'''
   return lex(example_code)