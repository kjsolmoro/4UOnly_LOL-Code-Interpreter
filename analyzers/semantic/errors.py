class LOLSemanticError(Exception):
  """Raised when a semantic / runtime error occurs in LOLCode."""
  pass


class BreakSignal(Exception):
  """Internal signal raised by GTFO to break out of loops, switch cases, or functions."""
  pass


class ReturnSignal(Exception):
  """Internal signal raised by FOUND YR inside functions. Carries the return value."""
  def __init__(self, value):
    self.value = value


class NeedsInputSignal(Exception):
  """Internal signal raised by GIMMEH when there is no input left. Carries the variable name."""
  def __init__(self, variable):
    self.variable = variable