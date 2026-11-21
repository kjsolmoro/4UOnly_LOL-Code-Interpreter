#==================================================================
# Executes statements and code blocks
#==================================================================
from analyzers.semantic.errors import LOLSemanticError, BreakSignal, ReturnSignal, NeedsInputSignal
from analyzers.semantic.typecast import to_yarn, cast_explicit
from analyzers.semantic import typecast
from analyzers.semantic.expressions import evaluate_expression
from analyzers.semantic import flow_control, functions


def execute_code_block(stmts, scope, runtime):
  """
  Executes a sequence of statement AST nodes.
  Iterates through stmts and calls execute_statement for each.
  """
  for stmt in stmts:
    execute_statement(stmt, scope, runtime)


def execute_statement(stmt, scope, runtime):
  """
  Dispatches an individual statement AST node to its execution logic:
  - "declare": exec_declare
  - "assign": exec_assign
  - "print": exec_print
  - "input": exec_input
  - "recast": exec_recast
  - "expression": evaluates expr and updates IT via set_it
  - "if_then", "switch", "loop": delegates to flow_control
  - "func_def", "func_return": delegates to functions
  """
  runtime["line"] = stmt["line"]
  stmt_type = stmt["type"]

  if stmt_type == "declare":
    exec_declare(stmt, scope, runtime)
  elif stmt_type == "assign":
    exec_assign(stmt, scope, runtime)
  elif stmt_type == "print":
    exec_print(stmt, scope, runtime)
  elif stmt_type == "input":
    exec_input(stmt, scope, runtime)
  elif stmt_type == "recast":
    exec_recast(stmt, scope, runtime)
  elif stmt_type == "expression":
    scope["IT"] = evaluate_expression(stmt["expr"], scope, runtime)
  elif stmt_type == "if_then":
    flow_control.execute_if_then(stmt, scope, runtime)
  elif stmt_type == "switch":
    flow_control.execute_switch(stmt, scope, runtime)
  elif stmt_type == "loop":
    flow_control.execute_loop(stmt, scope, runtime)
  elif stmt_type == "func_def":
    pass
  elif stmt_type == "func_return":
    functions.execute_func_return(stmt, scope, runtime)
  elif stmt_type == "break":
    raise BreakSignal()
  else:
    raise LOLSemanticError(f"Unknown statement type: {stmt_type}")

def check_declared(name, scope):
  if name not in scope:
    raise LOLSemanticError(f"variable '{name}' is not declared")
  

# ======================================================================
# INDIVIDUAL STATEMENT HANDLERS
# ======================================================================

def exec_declare(stmt, scope, runtime):
  """
  Handles variable declaration (I HAS A varident [ITZ expr]).
  Evaluates initializer if present, defaults to (None, "NOOB").
  Registers variable using declare_symbol.
  """
  runtime["line"] = stmt["line"]
  name = stmt["var"]
  if name in scope:
    raise LOLSemanticError(f"variable '{name}' is already declared")
  if stmt["init"] is None:
    scope[name] = None
  else:
    scope[name] = evaluate_expression(stmt["init"], scope, runtime)


def exec_assign(stmt, scope, runtime):
  """
  Handles variable assignment (varident R expr).
  Evaluates expression and updates variable using update_symbol.
  """
  check_declared(stmt["var"], scope)
  scope[stmt["var"]] = evaluate_expression(stmt["expr"], scope, runtime)


def exec_print(stmt, scope, runtime):
  """
  Handles VISIBLE statement.
  Evaluates all arguments, converts each to YARN via to_yarn,
  concatenates them, and appends the resulting string to interp["output"].
  """
  text = ""
  for arg in stmt["args"]:
    value = evaluate_expression(arg, scope, runtime)
    if value is None and typecast.VISIBLE_SHOWS_NOOB:
      text += "NOOB"
    else:
      text += to_yarn(value)
  runtime["output"].append(text + "\n")


def exec_input(stmt, scope, runtime):
  """
  Handles GIMMEH statement.
  Reads next available input from interp["inputs"] as YARN and updates variable.
  """
  raise LOLSemanticError("gawin muna GIMMEH")


def exec_recast(stmt, scope, runtime):
  """
  Handles IS NOW A recast statement (varident IS NOW A type).
  Performs explicit typecasting via cast_explicit and updates the variable.
  """
  raise LOLSemanticError("gawin muna IS NOW A")
