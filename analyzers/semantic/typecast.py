import re
from analyzers.semantic.errors import LOLSemanticError

VISIBLE_SHOWS_NOOB = True
COMPARE_NUMERIC_YARNS = False

def type_of(value):
  if value is None:
    return "NOOB"
  if type(value) == bool:
    return "TROOF"
  if type(value) == int:
    return "NUMBR"
  if type(value) == float:
    return "NUMBAR"
  return "YARN"

def is_number(value):
  return type_of(value) in ["NUMBR", "NUMBAR"]

# ======================================================================
# TYPECASTING & COERCION HELPERS
# ======================================================================

def to_troof(value):
  """
  Implicit/explicit cast to TROOF:
  - NOOB -> FAIL
  - TROOF -> value
  - NUMBR/NUMBAR -> FAIL if 0, else WIN
  - YARN -> FAIL if "", else WIN
  """
  if value is None:
    return False
  if type(value) == bool:
    return value
  if is_number(value):
    return value != 0
  return value != ""

def numbar_to_yarn(value):
  text = f"{value:.10f}"
  whole, decimals = text.split(".")
  return whole + "." + decimals[:2]

def to_yarn(value):
    kind = type_of(value)
    if kind == "NOOB":
      raise LOLSemanticError("cannot implicitly cast NOOB to a YARN")
    if kind == "TROOF":
      if value:
        return "WIN"
      else:
        return "FAIL"
    if kind == "NUMBR":
      return str(value)
    if kind == "NUMBAR":
      return numbar_to_yarn(value)
    return value

def yarn_to_number(text):
  """
  Implicit/explicit cast to YARN:
  - NOOB -> "NOOB" (or "" when explicit, handled in cast_explicit)
  - TROOF -> "WIN" or "FAIL"
  - NUMBR -> integer string
  - NUMBAR -> float string truncated to 2 decimals
  """
  if re.fullmatch(r'-?[0-9]+', text):
    return int(text)
  if re.fullmatch(r'-?[0-9]+\.[0-9]+', text):
    return float(text)
  return None


def to_num(value):
  """
  Implicit cast to numeric for arithmetic operations.
  Returns (numeric_value, "NUMBR" | "NUMBAR").
  NOOB cannot be implicitly cast to numeric -> raises LOLSemanticError.
  """
  kind = type_of(value)
  if kind == "NOOB":
    raise LOLSemanticError("cannot implicitly cast NOOB to a number")

  if kind == "TROOF":
    return 1 if value else 0

  if kind == "NUMBR":
    return value

  if kind == "NUMBAR":
    return value

  number = yarn_to_number(value)
  if number == None:
    raise LOLSemanticError(f"cannot cast YARN \"{value}\" to a number")

  return number


def cast_explicit(value, target_type):
  """
  Explicit typecasting via MAEK or IS NOW A:
  - Target types: NOOB, TROOF, NUMBR, NUMBAR, YARN
  """
  if target_type == "NOOB":
    return None

  if target_type == "TROOF":
    return (to_troof(value))

  if target_type == "NUMBR":
    if value is None:
      return 0
    return int(to_num(value))

  if target_type == "NUMBAR":
    if value is None:
      return 0.0
    return float(to_num(value))

  if target_type == "YARN":
    if value is None:
      return ""
    return to_yarn(value)

  raise LOLSemanticError(f"Invalid target type for typecasting: '{target_type}'")


# FOR SYMVBOL TABLE DISPLAY ONLY
def format_value(value):
  if value is None:
    return "NOOB"
  return to_yarn(value)