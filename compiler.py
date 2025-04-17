from typing import List

import lexer
import loader
import util
from loader import Function, LimboFunction

from parser import Parser

class CompiledFunction(Function):
   pass

def compile_code(code: str, debug: bool):
   tokens = lexer.lex(code)
   parser = Parser(tokens, debug, util.Logging.change_log_format("Parser"))
   ast = parser.parse()
   return ast

def compile_func(func: LimboFunction, debug: bool):
   return compile_code(func.code, debug)

def from_file(filename: str, debug=False) -> List[CompiledFunction]:
   with open(filename, "r") as file:
      code = file.read()
   _, functions = loader.extract_functions(code)
   functions: List[loader.LimboFunction]
   return [CompiledFunction(func.name, compile_func(func, debug)) for func in functions]
