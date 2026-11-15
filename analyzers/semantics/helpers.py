#(OwO)==================================================================
# Contains Type coercion, symbol table management, and semantic exceptions
#(OwO)==================================================================

class LOLSemanticError(Exception):
  """Raised when a semantic / runtime error occurs in LOLCode."""
  pass

class BreakSignal(Exception):
  """Internal signal raised by GTFO to break out of loops or switch cases."""
  pass

class ReturnSignal(Exception):
  """Internal signal raised by FOUND YR or GTFO inside functions."""
  def __init__(self, value, type_name):
    self.value = value
    self.type_name = type_name

class NeedsInputSignal(Exception):
  """
  Raised when GIMMEH needs input from the user but none is currently available.
  Allows interactive prompt loops between the frontend and backend.
  """
  def __init__(self, var_name):
    self.var_name = var_name