from analyzers.semantic.errors import LOLSemanticError, BreakSignal, ReturnSignal, NeedsInputSignal
from analyzers.semantic.typecast import type_of, format_value
from analyzers.semantic.statements import execute_code_block, exec_declare
from analyzers.semantic.functions import register_function


def run(ast, inputs=None):
  runtime = {
    "functions": {},
    "output": [],
    "inputs": inputs or [],
    "next_input": 0,
    "line": 0,
  }
  scope = {"IT": None}
  errors = []
  need_input = None

  try:
    for func_node in all_functions(ast):
      register_function(func_node, runtime)
    for declaration in ast["declarations"]:
      exec_declare(declaration, scope, runtime)
    execute_code_block(ast["body"], scope, runtime)
  except NeedsInputSignal as signal:
    need_input = signal.variable
  except LOLSemanticError as e:
    errors.append(error_message(runtime, str(e)))
  except BreakSignal:
    errors.append(error_message(runtime, "GTFO used outside a loop, switch, or function"))
  except ReturnSignal:
    errors.append(error_message(runtime, "FOUND YR used outside a function"))

  return {
    "output": "".join(runtime["output"]),
    "symbols": symbol_table(scope),
    "errors": errors,
    "need_input": need_input,
  }


def all_functions(ast):
  # functions before HAI / after KTHXBYE are in ast["functions"],
  # functions written inside the main body are "func_def" statements
  found = list(ast["functions"])
  for node in ast["body"]:
    if node["type"] == "func_def":
      found.append(node)
  return found


def error_message(runtime, message):
  return f"Line {runtime['line']}: Semantic Error: {message}"


def symbol_table(scope):
  rows = []
  for name, value in scope.items():
    rows.append({"identifier": name, "value": format_value(value), "type": type_of(value)})
  return rows