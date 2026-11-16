#(OwO)==================================================================
# FUNCTION EXECUTOR
# Handles function definition registration, isolated scoping, calls, and returns
#(OwO)==================================================================
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
  Raises a ReturnSignal carrying the result and its type.
  """
  pass


def eval_func_call(interp, call_node):
  """
  Executes a function call: I IZ <func> [YR arg ...] [MKAY]
  - Verifies function existence and parameter count.
  - Evaluates argument expressions in the caller's context (pass-by-value).
  - Creates a completely isolated local symbol table for the function call.
  - Parameters become local variables initialized with the evaluated arguments.
  - Handles return via ReturnSignal (or GTFO via BreakSignal returning NOOB).
  - Restores caller's symbol table upon completion.
  - Automatically stores the return value in the caller's IT.
  """
  pass
