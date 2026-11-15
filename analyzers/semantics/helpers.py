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
  
# ======================================================================
# SYMBOL TABLE HELPERS
# ======================================================================

def declare_symbol(interp, name, value=None, type_name="NOOB"):
  """Declares a new variable in the current symbol table scope."""
  if name in interp["symbols"]:
    raise LOLSemanticError(f"Variable '{name}' already declared in current scope")
  interp["symbols"][name] = {"type": type_name, "value": value}


def get_symbol(interp, name):
  """Retrieves a variable dictionary from the current scope."""
  if name in interp["symbols"]:
    return interp["symbols"][name]
  raise LOLSemanticError(f"Variable '{name}' has not been declared")


def update_symbol(interp, name, value, type_name):
  """Updates an existing variable's value and type in the current scope."""
  if name not in interp["symbols"]:
    raise LOLSemanticError(f"Cannot assign to undeclared variable '{name}'")
  interp["symbols"][name] = {"type": type_name, "value": value}


def set_it(interp, value, type_name):
  """Updates the implicit IT variable in the current scope."""
  interp["symbols"]["IT"] = {"type": type_name, "value": value}


def get_it(interp):
  """Returns the current (value, type) of IT."""
  it_entry = interp["symbols"].get("IT", {"type": "NOOB", "value": None})
  return it_entry["value"], it_entry["type"]


def format_value(value, type_name):
  """Formats a runtime value into its user-facing LOLCode string."""
  if type_name == "NOOB" or value is None:
    return "NOOB"
  if type_name == "TROOF":
    return "WIN" if value else "FAIL"
  if type_name == "NUMBAR":
    # Truncate to up to two decimal places if needed
    val_str = str(value)
    parts = val_str.split('.')
    if len(parts) == 2 and len(parts[1]) > 2:
      return f"{parts[0]}.{parts[1][:2]}"
    return val_str
  return str(value)


def snapshot_symbols(interp):
  """Returns a list of dicts for the frontend Symbol Table."""
  result = []
  # IT is always first
  if "IT" in interp["symbols"]:
    it_entry = interp["symbols"]["IT"]
    result.append({
      "identifier": "IT",
      "type": it_entry["type"],
      "value": format_value(it_entry["value"], it_entry["type"])
    })

  for name, entry in interp["symbols"].items():
    if name == "IT":
      continue
    result.append({
      "identifier": name,
      "type": entry["type"],
      "value": format_value(entry["value"], entry["type"])
    })
  return result