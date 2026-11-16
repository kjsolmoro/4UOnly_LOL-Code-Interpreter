#==================================================================
# Contains Type coercion, symbol table 
#==================================================================

class LOLSemanticError(Exception):
  """Raised when a semantic / runtime error occurs in LOLCode."""
  pass

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

# ======================================================================
# TYPECASTING & COERCION HELPERS
# ======================================================================

def to_troof(value, type_name):
  """
  Implicit/explicit cast to TROOF:
  - NOOB -> FAIL
  - TROOF -> value
  - NUMBR/NUMBAR -> FAIL if 0, else WIN
  - YARN -> FAIL if "", else WIN
  """
  if type_name == "NOOB" or value is None:
    return False
  if type_name == "TROOF":
    return bool(value)
  if type_name in ["NUMBR", "NUMBAR"]:
    return value != 0
  if type_name == "YARN":
    return len(value) > 0
  return bool(value)


def to_yarn(value, type_name):
  """
  Implicit/explicit cast to YARN:
  - NOOB -> "NOOB" (or "" when explicit, handled in cast_explicit)
  - TROOF -> "WIN" or "FAIL"
  - NUMBR -> integer string
  - NUMBAR -> float string truncated to 2 decimals
  """
  return format_value(value, type_name)


def to_num(value, type_name):
  """
  Implicit cast to numeric for arithmetic operations.
  Returns (numeric_value, "NUMBR" | "NUMBAR").
  NOOB cannot be implicitly cast to numeric -> raises LOLSemanticError.
  """
  if type_name == "NOOB" or value is None:
    raise LOLSemanticError("Cannot implicitly cast NOOB to a numerical type")

  if type_name == "TROOF":
    return (1 if value else 0, "NUMBR")

  if type_name == "NUMBR":
    return (int(value), "NUMBR")

  if type_name == "NUMBAR":
    return (float(value), "NUMBAR")

  if type_name == "YARN":
    s = value.strip()
    # Try integer first
    try:
      return (int(s), "NUMBR")
    except ValueError:
      pass
    # Try float
    try:
      return (float(s), "NUMBAR")
    except ValueError:
      raise LOLSemanticError(f"Cannot cast YARN \"{value}\" to a numerical type")

  raise LOLSemanticError(f"Unsupported type '{type_name}' for numerical operation")


def cast_explicit(value, from_type, target_type):
  """
  Explicit typecasting via MAEK or IS NOW A:
  - Target types: NOOB, TROOF, NUMBR, NUMBAR, YARN
  """
  if target_type == "NOOB":
    return (None, "NOOB")

  if target_type == "TROOF":
    if from_type == "NOOB":
      return (False, "TROOF")
    return (to_troof(value, from_type), "TROOF")

  if target_type == "NUMBR":
    if from_type == "NOOB":
      return (0, "NUMBR")
    val, _ = to_num(value, from_type)
    return (int(val), "NUMBR")

  if target_type == "NUMBAR":
    if from_type == "NOOB":
      return (0.0, "NUMBAR")
    val, _ = to_num(value, from_type)
    return (float(val), "NUMBAR")

  if target_type == "YARN":
    if from_type == "NOOB":
      return ("", "YARN")
    return (to_yarn(value, from_type), "YARN")

  raise LOLSemanticError(f"Invalid target type for typecasting: '{target_type}'")
