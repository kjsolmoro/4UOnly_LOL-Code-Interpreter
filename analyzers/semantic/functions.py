#==================================================================
# Handles function definition registration, isolated scoping, calls, and returns
#==================================================================
from analyzers.semantics.helpers import (
  LOLSemanticError,
  BreakSignal,
  ReturnSignal,
  set_it,
)
from analyzers.semantics.expressions import evaluate_expression


def register_function(interp, func_node):
  """
  Registers a function definition into the interpreter's function table (interp["functions"]).
  """
  pass


def execute_func_return(interp, stmt):
  """
  FOUND YR <expression> returns the evaluated value of the expression.
  """
  pass


def eval_func_call(interp, call_node):
  """
  Executes a function call: I IZ <func> [YR arg ...] [MKAY]
  - Evaluates argument expressions
  - Creates a local symbol table for the function call.
  - Automatically stores the return value in the caller's IT.
  """
  pass
