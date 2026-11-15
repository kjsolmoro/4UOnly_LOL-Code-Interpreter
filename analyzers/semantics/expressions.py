#==================================================================
# Evaluates all expression AST nodes and returns (value, type_name)
#==================================================================
from analyzers.semantics.helpers import (LOLSemanticError,  declare_symbol,  get_symbol,  update_symbol,  to_troof,  to_yarn,  to_num,
  cast_explicit, )

def evaluate_expression(interp, node):
  """Dispatches and evaluates any expression AST node."""
  if node is None:
    return (None, "NOOB")

  # Literals and Variable Identifiers
  if isinstance(node, (tuple, list)):
    lexeme, classification, line = node

    if classification == "NUMBR Literal":
      return (int(lexeme), "NUMBR")

    elif classification == "NUMBAR Literal":
      return (float(lexeme), "NUMBAR")

    elif classification == "YARN Literal":
      if lexeme.startswith('"') and lexeme.endswith('"'):
        return (lexeme[1:-1], "YARN")
      return (lexeme, "YARN")

    elif classification == "TROOF Literal":
      return (True if lexeme == "WIN" else False, "TROOF")

    elif classification == "TYPE Literal":
      return (lexeme, "TYPE")

    elif classification == "Variable Identifier":
      entry = get_symbol(interp, lexeme)
      return (entry["value"], entry["type"])

    else:
      raise LOLSemanticError(f"Line {line}: Cannot evaluate token '{lexeme}'")

  # Dictionary
  node_type = node.get("type")

  if node_type == "arithmetic":
    return eval_arithmetic(interp, node)

  elif node_type == "boolean_binary":
    return eval_boolean_binary(interp, node)

  elif node_type == "boolean_unary":
    return eval_boolean_unary(interp, node)

  elif node_type == "comparison":
    return eval_comparison(interp, node)

  elif node_type == "concat":
    return eval_concat(interp, node)

  elif node_type == "infinite_bool":
    return eval_infinite_bool(interp, node)

  elif node_type == "typecast":
    return eval_typecast(interp, node)

  elif node_type == "func_call":
    from analyzers.semantics import functions
    return functions.eval_func_call(interp, node)

  else:
    raise LOLSemanticError(f"Unknown expression node type: {node_type}")

# ======================================================================
# INDIVIDUAL EXPRESSION EVALUATORS
# ======================================================================

def _get_op_lexeme(op_obj):
  if isinstance(op_obj, (tuple, list)):
    return op_obj[0]
  return str(op_obj)


def eval_arithmetic(interp, node):
  op = _get_op_lexeme(node["op"])
  left_val, left_type = evaluate_expression(interp, node["left"])
  right_val, right_type = evaluate_expression(interp, node["right"])

  n1, t1 = to_num(left_val, left_type)
  n2, t2 = to_num(right_val, right_type)

  # If at least one operand is NUMBAR, the result is NUMBAR
  is_float = (t1 == "NUMBAR" or t2 == "NUMBAR")

  if op == "SUM OF":
    res = n1 + n2
  elif op == "DIFF OF":
    res = n1 - n2
  elif op == "PRODUKT OF":
    res = n1 * n2
  elif op == "QUOSHUNT OF":
    if n2 == 0:
      raise LOLSemanticError("Division by zero in QUOSHUNT OF")
    if is_float:
      res = n1 / n2
    else:
      res = n1 // n2
  elif op == "MOD OF":
    if n2 == 0:
      raise LOLSemanticError("Modulo by zero in MOD OF")
    res = n1 % n2
  elif op == "BIGGR OF":
    res = max(n1, n2)
  elif op == "SMALLR OF":
    res = min(n1, n2)
  else:
    raise LOLSemanticError(f"Unknown arithmetic operator: '{op}'")

  if is_float:
    return (float(res), "NUMBAR")
  return (int(res), "NUMBR")

def eval_boolean_binary(interp, node):
  op = _get_op_lexeme(node["operator"])
  left_val, left_type = evaluate_expression(interp, node["left"])
  right_val, right_type = evaluate_expression(interp, node["right"])

  b1 = to_troof(left_val, left_type)
  b2 = to_troof(right_val, right_type)

  if op == "BOTH OF":
    res = b1 and b2
  elif op == "EITHER OF":
    res = b1 or b2
  elif op == "WON OF":
    res = (b1 != b2)
  else:
    raise LOLSemanticError(f"Unknown boolean operator: '{op}'")

  return (res, "TROOF")


def eval_boolean_unary(interp, node):
  operand_val, operand_type = evaluate_expression(interp, node["operand"])
  b = to_troof(operand_val, operand_type)
  return (not b, "TROOF")


def eval_comparison(interp, node):
  op = _get_op_lexeme(node["operator"])
  left_val, left_type = evaluate_expression(interp, node["left"])
  right_val, right_type = evaluate_expression(interp, node["right"])

  # If both are numbers (NUMBR and/or NUMBAR), numeric comparison applies
  if left_type in ["NUMBR", "NUMBAR"] and right_type in ["NUMBR", "NUMBAR"]:
    equal = (left_val == right_val)
  elif left_type != right_type:
    # Mismatched non-numeric types are not equal
    equal = False
  else:
    equal = (left_val == right_val)

  if op == "BOTH SAEM":
    return (equal, "TROOF")
  elif op == "DIFFRINT":
    return (not equal, "TROOF")
  else:
    raise LOLSemanticError(f"Unknown comparison operator: '{op}'")


def eval_concat(interp, node):
  # SMOOSH concatenates all operands after converting each to YARN
  parts = []
  for op_node in node["operands"]:
    val, typ = evaluate_expression(interp, op_node)
    parts.append(to_yarn(val, typ))
  return ("".join(parts), "YARN")


def eval_infinite_bool(interp, node):
  op = _get_op_lexeme(node["operator"])
  bool_values = []
  for op_node in node["operands"]:
    val, typ = evaluate_expression(interp, op_node)
    bool_values.append(to_troof(val, typ))

  if op == "ALL OF":
    res = all(bool_values)
  elif op == "ANY OF":
    res = any(bool_values)
  else:
    raise LOLSemanticError(f"Unknown infinite bool operator: '{op}'")

  return (res, "TROOF")


def eval_typecast(interp, node):
  val, typ = evaluate_expression(interp, node["operand"])
  target_token = node["target_type"]
  target_type = _get_op_lexeme(target_token)
  return cast_explicit(val, typ, target_type)
