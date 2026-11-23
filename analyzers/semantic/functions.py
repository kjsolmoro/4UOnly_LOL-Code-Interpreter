#==================================================================
# Handles function definition registration, isolated scoping, calls, and returns
#==================================================================
from analyzers.semantic.errors import LOLSemanticError, BreakSignal, ReturnSignal
from analyzers.semantic.expressions import evaluate_expression
from analyzers.semantic import statements

# Limiter depth value for recursive calls (LoL)
MAX_CALL_DEPTH = 100

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

  value = evaluate_expression(stmt["expr"], scope, runtime)
  raise ReturnSignal(value)

  # raise LOLSemanticError("gawin muna FOUND YR")


def eval_func_call(call_node, scope, runtime):
  """
  Executes a function call: I IZ <func> [YR arg ...] [MKAY]
  - Evaluates argument expressions
  - Creates a local symbol table for the function call.
  - Automatically stores the return value in the caller's IT.
  """

  name = call_node["name"]
  if name not in runtime["functions"]:
    raise LOLSemanticError(f"function '{name}' is not defined")

  func = runtime["functions"][name]
  params = func["params"]
  args = call_node["args"]

  if len(args) != len(params):
    raise LOLSemanticError(f"function '{name}' expects {len(params)} argument(s) but got {len(args)}")

  values = [] # args use caller's scope (PoP)
  for arg in args:
    values.append(evaluate_expression(arg, scope, runtime))

  depth = runtime.get("depth", 0)
  if depth >= MAX_CALL_DEPTH:
    raise LOLSemanticError(f"function '{name}' called itself too many times")

  # local IT and params exist inside
  local_scope = {"IT": None}
  for i in range(len(params)):
    local_scope[params[i]] = values[i]

  call_line = runtime["line"]
  runtime["depth"] = depth + 1

  # default value if no return statement (UwU) this means no FOUND YR or GTFO
  # return null or NOOB
  result = None

  try:
    statements.execute_code_block(func["body"], local_scope, runtime)
  except ReturnSignal as signal:
    result = signal.value
  except BreakSignal:
    result = None
  runtime["depth"] = depth
  runtime["line"] = call_line

  # (OwO) BALI it means it is return to whoever called this to its IT value
  # Reminder: every func has its own local implicit IT na don nagsstore muna ng var
  scope["IT"] = result
  return result

  # raise LOLSemanticError("gawin muna function calls")

