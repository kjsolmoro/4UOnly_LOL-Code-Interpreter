#==================================================================
# Handles function definition registration, isolated scoping, calls, and returns
#==================================================================
from analyzers.semantic.errors import LOLSemanticError, BreakSignal, ReturnSignal
from analyzers.semantic.expressions import evaluate_expression
from analyzers.semantic import statements


def register_function(func_node, runtime):
  """
  Registers a function definition into the interpreter's function table (interp["functions"]).
  """
  name = func_node["name"]
  if name in runtime["functions"]:
    raise LOLSemanticError(f"function '{name}' is already defined")
  runtime["functions"][name] = func_node

def execute_func_return(stmt, scope, runtime):
  """
  FOUND YR <expression> returns the evaluated value of the expression.
  """
  raise LOLSemanticError("gawin muna FOUND YR")


def eval_func_call(call_node, scope, runtime):
  """
  Executes a function call: I IZ <func> [YR arg ...] [MKAY]
  - Evaluates argument expressions
  - Creates a local symbol table for the function call.
  - Automatically stores the return value in the caller's IT.
  """
  raise LOLSemanticError("gawin muna function calls")

