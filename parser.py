class ASTNode:
   def __repr__(self):
      return f"{self.__class__.__name__}{self.__dict__}"

# Expressions (literals, identifiers, arithmetic)
class VariableDeclaration(ASTNode):
   def __init__(self, name, value):
      self.name = name
      self.value = value

class Assignment(ASTNode):
   def __init__(self, name, value):
      self.name = name
      self.value = value

class IfStatement(ASTNode):
   def __init__(self, condition, if_block, else_if_blocks, else_block):
      self.condition = condition
      self.if_block = if_block
      self.else_if_blocks = else_if_blocks
      self.else_block = else_block

class WhileLoop(ASTNode):
   def __init__(self, condition, body):
      self.condition = condition
      self.body = body

class BinaryOperation(ASTNode):
   def __init__(self, left, operator, right):
      self.left = left
      self.operator = operator
      self.right = right

class UnaryOperation(ASTNode):
   def __init__(self, operator, operand):
      self.operator = operator
      self.operand = operand

class FunctionCall(ASTNode):
   def __init__(self, function, args):
      self.function = function
      self.args = args

class Literal(ASTNode):
   def __init__(self, value):
      self.value = value

class Identifier(ASTNode):
   def __init__(self, name):
      self.name = name

class Condition:
   def __init__(self, left, op, right):
      self.left = left
      self.op = op
      self.right = right

   def __repr__(self):
      return f"({self.left} {self.op} {self.right})"


# Parsing functions

class Parser:
   def __init__(self, tokens, debug=False, logger=None):
      self.tokens = tokens
      self.pos = 0
      self.current_token = self.tokens[self.pos]
      self.debug = debug
      self.logger = logger
      if self.debug and not self.logger:
         raise ValueError("Debug mode enabled but logger not provided!")

   def peek(self, offset=1):
      if self.debug:
         self.logger.debug(f"Peeking with offset {offset}")
      if self.pos + offset < len(self.tokens):
         return self.tokens[self.pos + offset]
      return None

   def consume(self):
      if self.debug:
         self.logger.debug(f"Consuming token: {self.current_token}")
      self.pos += 1
      if self.pos < len(self.tokens):
         self.current_token = self.tokens[self.pos]
      else:
         self.current_token = None

   def expect(self, token_type):
      if self.debug:
         self.logger.debug(f"Expecting token type: {token_type}, current: {self.current_token}")
      if self.current_token and self.current_token.type == token_type:
         value = self.current_token.value
         self.consume()
         return value
      else:
         raise SyntaxError(f"Expected {token_type} but got {self.current_token.type}")

   def parse(self):
      if self.debug:
         self.logger.debug("Starting parse")
      statements = []
      while self.current_token:
         statements.append(self.parse_statement())
      if self.debug:
         self.logger.debug("Completed parse")
      return statements

   def parse_statement(self):
      if self.debug:
         self.logger.debug(f"Parsing statement, current token: {self.current_token}")
      if self.current_token.type == "LET":
         return self.parse_variable_declaration()
      elif self.current_token.type == "IF":
         return self.parse_if_statement()
      elif self.current_token.type == "WHILE":
         return self.parse_while_loop()
      elif self.current_token.type == "IDENT":
         next_token = self.peek()
         if next_token and next_token.type == "LPAREN":
            return self.parse_function_call()
         else:
            return self.parse_assignment()
      else:
         raise SyntaxError(f"Unexpected token: {self.current_token}")

   def parse_variable_declaration(self):
      if self.debug:
         self.logger.debug("Parsing variable declaration")
      self.expect("LET")
      name = self.expect("IDENT")
      self.expect("ASSIGN")
      value = self.parse_expression()
      self.expect("SEMICOLON")
      return VariableDeclaration(name, value)

   def parse_assignment(self):
      if self.debug:
         self.logger.debug("Parsing assignment")

      name = self.expect("IDENT")

      if self.current_token and self.current_token.type in ["INCREMENT", "DECREMENT"]:
         operator = "DECREMENT" if self.current_token.value == "--" else "INCREMENT"
         self.consume()
         self.expect("SEMICOLON")
         return UnaryOperation(operator, Identifier(name))

      if self.current_token and self.current_token.type in ["ADD_ASSIGN", "SUB_ASSIGN", "MUL_ASSIGN", "DIV_ASSIGN"]:
         operator = self.current_token.value
         self.consume()
         right = self.parse_expression()
         self.expect("SEMICOLON")
         return Assignment(name, BinaryOperation(Identifier(name), operator, right))  # Strip "_ASSIGN"

      self.expect("ASSIGN")
      value = self.parse_expression()
      self.expect("SEMICOLON")
      return Assignment(name, value)

   def parse_if_statement(self):
      if self.debug:
         self.logger.debug("Parsing if statement")
      self.expect("IF")
      self.expect("LPAREN")
      condition = self.parse_condition()
      self.expect("RPAREN")
      self.expect("LBRACE")
      if_block = self.parse_block()
      self.expect("RBRACE")

      else_if_blocks = []
      while self.current_token and self.current_token.type == "ELSE":
         self.consume()
         if self.current_token.type == "IF":
            self.consume()
            self.expect("LPAREN")
            else_condition = self.parse_condition()
            self.expect("RPAREN")
            self.expect("LBRACE")
            else_if_block = self.parse_block()
            self.expect("RBRACE")
            else_if_blocks.append((else_condition, else_if_block))
         else:
            self.expect("LBRACE")
            else_block = self.parse_block()
            self.expect("RBRACE")
            else_if_blocks.append((None, else_block))
            break

      return IfStatement(condition, if_block, else_if_blocks, None)

   def parse_while_loop(self):
      if self.debug:
         self.logger.debug("Parsing while loop")
      self.expect("WHILE")
      self.expect("LPAREN")
      condition = self.parse_condition()
      self.expect("RPAREN")
      self.expect("LBRACE")
      body = self.parse_block()
      self.expect("RBRACE")
      return WhileLoop(condition, body)

   def parse_expression(self):
      if self.debug:
         self.logger.debug("Parsing expression")
      left = self.parse_term()
      while self.current_token and self.current_token.type in ("PLUS", "MINUS"):
         operator = self.current_token.value
         self.consume()
         right = self.parse_term()
         left = BinaryOperation(left, operator, right)
      return left

   def parse_term(self):
      if self.debug:
         self.logger.debug("Parsing term")
      left = self.parse_factor()
      while self.current_token and self.current_token.type in ("MUL", "DIV", "EXPONENT", "INT_DIV"):
         operator = self.current_token.value
         self.consume()
         right = self.parse_factor()
         left = BinaryOperation(left, operator, right)
      return left

   def parse_factor(self):
      if self.debug:
         self.logger.debug("Parsing factor")
      if self.current_token.type == "NUMBER":
         value = self.expect("NUMBER")
         return Literal(value)
      elif self.current_token.type == "STRING":
         value = self.expect("STRING")
         return Literal(value)
      elif self.current_token.type == "IDENT":
         return Identifier(self.expect("IDENT"))
      elif self.current_token.type == "LPAREN":
         self.expect("LPAREN")
         expr = self.parse_expression()
         self.expect("RPAREN")
         return expr
      elif self.current_token.type == "MINUS":
         self.consume()
         operand = self.parse_factor()
         return UnaryOperation("MINUS", operand)
      elif self.current_token.type == "PLUS":
         self.consume()
         operand = self.parse_factor()
         return UnaryOperation("PLUS", operand)

   def parse_block(self):
      if self.debug:
         self.logger.debug("Parsing block")
      statements = []
      while self.current_token and self.current_token.type != "RBRACE":
         statements.append(self.parse_statement())
      return statements

   def parse_condition(self):
      if self.debug:
         self.logger.debug("Parsing condition")
      left = self.parse_expression()

      if self.current_token and self.current_token.type in {
         "EQ", "NEQ", "LT", "GT", "LTE", "GTE"
      }:
         op = self.current_token.type
         self.consume()
         right = self.parse_expression()
         return Condition(left, op, right)
      else:
         # Just return the expression if there's no comparison
         return left

   def parse_function_call(self):
      if self.debug:
         self.logger.debug(f"Parsing function")
      name = self.expect("IDENT")
      self.expect("LPAREN")
      args = []

      if self.current_token.type != "RPAREN":
         while True:
            arg = self.parse_expression()
            args.append(arg)
            if self.current_token.type == "COMMA":
               self.consume()
            else:
               break

      self.expect("RPAREN")
      self.expect("SEMICOLON")
      return FunctionCall(name, args)
