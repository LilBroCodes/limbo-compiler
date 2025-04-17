import re

class Token:
   def __init__(self, token_type: str, value: str, line: int, col: int):
      self.type = token_type
      self.value = value
      self.line = line
      self.col = col

   def __repr__(self):
      return f"{self.type}({repr(self.value)}) @ {self.line}:{self.col}"


# Token specification with regex patterns
TOKEN_SPEC = [
   # Keywords
   ("LET", r"\blet\b"),
   ("IF", r"\bif\b"),
   ("ELSE", r"\belse\b"),
   ("WHILE", r"\bwhile\b"),

   # Operators
   ("ADD_ASSIGN", r"\+="),
   ("SUB_ASSIGN", r"-="),
   ("MUL_ASSIGN", r"\*="),
   ("DIV_ASSIGN", r"/="),
   ("INCREMENT", r"\+\+"),
   ("DECREMENT", r"--"),
   ("EXPONENT", r"\*\*"),
   ("INT_DIV", r"//"),
   ("EQ", r"=="),
   ("NEQ", r"!="),
   ("LTE", r"<="),
   ("GTE", r">="),
   ("ASSIGN", r"="),
   ("LT", r"<"),
   ("GT", r">"),
   ("PLUS", r"\+"),
   ("MINUS", r"-"),
   ("MUL", r"\*"),
   ("DIV", r"/"),

   # Punctuation
   ("LPAREN", r"\("),
   ("RPAREN", r"\)"),
   ("LBRACE", r"\{"),
   ("RBRACE", r"\}"),
   ("SEMICOLON", r";"),
   ("COMMA", r","),

   # Literals
   ("STRING", r'"(?:\\.|[^"\\])*"'),
   ("NUMBER", r"\d+(\.\d+)?"),

   # Identifiers
   ("IDENT", r"[a-zA-Z_][a-zA-Z0-9_]*"),

   # Comments (skipped)
   ("LINE_COMMENT", r"#[^\n]*"),
   ("BLOCK_COMMENT", r"/\*[\s\S]*?\*/"),

   # Whitespace (skipped)
   ("WHITESPACE", r"\s+"),
]

# Combine the individual regex patterns into one big regex
TOKEN_REGEX = "|".join(f'(?P<{name}>{regex})' for name, regex in TOKEN_SPEC)
TOKEN_RE = re.compile(TOKEN_REGEX, re.DOTALL)


def lex(code: str):
   tokens = []
   line_num = 1
   line_start = 0

   # Iterate over matches in the source code
   for match in TOKEN_RE.finditer(code):
      kind = match.lastgroup
      value = match.group()
      start_pos = match.start()
      column = start_pos - line_start

      # Count how many newlines are in the current match
      newline_count = value.count("\n")

      # Skip whitespace, comments, and block comments
      if kind == "WHITESPACE" or kind in ("LINE_COMMENT", "BLOCK_COMMENT"):
         if newline_count:
            line_num += newline_count
            last_newline = value.rfind("\n")
            line_start = start_pos + last_newline + 1
         continue

      # If the token is valid (i.e., it's not whitespace or a comment)
      tokens.append(Token(kind, value, line_num, column))

      # Update line number and start position if the token contains newlines
      if newline_count:
         line_num += newline_count
         last_newline = value.rfind("\n")
         line_start = start_pos + last_newline + 1

   return tokens
