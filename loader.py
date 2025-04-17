import re
from typing import List

class Function:
    def __init__(self, name: str, code: str):
        self.name = name
        self.code = code

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name})"


class VanillaFunction(Function):
    pass


class LimboFunction(Function):
    pass


def extract_functions(code: str) -> (List[VanillaFunction], List[LimboFunction]):
   pattern = re.compile(r'\b(fun|def)\s+(\w+)\s*\(([^)]*)\)\s*{', re.MULTILINE)
   vanilla_funcs = []
   limbo_funcs = []

   for match in pattern.finditer(code):
      kind = match.group(1)
      name = match.group(2)
      start_index = match.end()  # Start after the opening '{'
      brace_count = 1
      i = start_index

      while i < len(code):
         if code[i] == '{':
            brace_count += 1
         elif code[i] == '}':
            brace_count -= 1
            if brace_count == 0:
               break
         i += 1

      inner_code = code[start_index:i].strip()  # Only code inside { }

      if kind == "fun":
         vanilla_funcs.append(VanillaFunction(name, inner_code))
      else:
         limbo_funcs.append(LimboFunction(name, inner_code))

   return vanilla_funcs, limbo_funcs
