#==================================================================
# Evaluates all expression AST nodes and returns (value, type_name)
#==================================================================
import math
from analyzers.semantic.errors import LOLSemanticError
from analyzers.semantic.typecast import to_troof, to_yarn, to_num, cast_explicit, is_number, type_of, yarn_to_number
from analyzers.semantic import typecast 

def evaluate_expression(node, scope, runtime):
  """Dispatches and evaluates any expression AST node."""
  if node is None:
    return None

  # Literals and Variable Identifiers
  if isinstance(node, (tuple, list)):
    lexeme, classification, line = node

    if classification == "NUMBR Literal":
      return int(lexeme)

    elif classification == "NUMBAR Literal":
      return float(lexeme)

    elif classification == "YARN Literal":
      if lexeme.startswith('"') and lexeme.endswith('"'):
        return lexeme[1:-1]
      return lexeme

    elif classification == "TROOF Literal":
      return True if lexeme == "WIN" else False

    elif classification == "TYPE Literal":
      return lexeme

    elif classification == "Variable Identifier":
      if lexeme not in scope:
        raise LOLSemanticError(f"variable '{lexeme}' is not declared")
      return scope[lexeme]

    else:
      raise LOLSemanticError(f"Cannot evaluate token '{lexeme}'")

  # Dictionary
  node_type = node.get("type")

  if node_type == "arithmetic":
    return eval_arithmetic(node, scope, runtime)

  elif node_type == "boolean_binary":
    return eval_boolean_binary(node, scope, runtime)

  elif node_type == "boolean_unary":
    return eval_boolean_unary(node, scope, runtime)

  elif node_type == "comparison":
    return eval_comparison(node, scope, runtime)

  elif node_type == "concat":
    return eval_concat(node, scope, runtime)

  elif node_type == "infinite_bool":
    return eval_infinite_bool(node, scope, runtime)

  elif node_type == "typecast":
    return eval_typecast(node, scope, runtime)

  elif node_type == "func_call":
    from analyzers.semantic import functions
    return functions.eval_func_call(node, scope, runtime)

  else:
    raise LOLSemanticError(f"Unknown expression node type: {node_type}")

# ======================================================================
# INDIVIDUAL EXPRESSION EVALUATORS
# ======================================================================

def _get_op_lexeme(op_obj):
  if isinstance(op_obj, (tuple, list)):
    return op_obj[0]
  return str(op_obj)


def eval_arithmetic(node, scope, runtime):
  op = _get_op_lexeme(node["op"])
  left_val = evaluate_expression(node["left"], scope, runtime)
  right_val = evaluate_expression(node["right"], scope, runtime)

  n1 = to_num(left_val)
  n2 = to_num(right_val)

  # If at least one operand is NUMBAR, the result is NUMBAR
  is_float = (type(n1) == float or type(n2) == float)

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
      res = int(n1 / n2)
  elif op == "MOD OF":
    if n2 == 0:
      raise LOLSemanticError("Modulo by zero in MOD OF")
    res = math.fmod(n1,n2)
  elif op == "BIGGR OF":
    res = max(n1, n2)
  elif op == "SMALLR OF":
    res = min(n1, n2)
  else:
    raise LOLSemanticError(f"Unknown arithmetic operator: '{op}'")

  if is_float:
    return float(res)
  return int(res)

def eval_boolean_binary(node, scope, runtime):
  op = _get_op_lexeme(node["operator"])
  left_val = evaluate_expression(node["left"], scope, runtime)
  right_val = evaluate_expression(node["right"], scope, runtime)

  b1 = to_troof(left_val)
  b2 = to_troof(right_val)

  if op == "BOTH OF":
    res = b1 and b2
  elif op == "EITHER OF":
    res = b1 or b2
  elif op == "WON OF":
    res = (b1 != b2)
  else:
    raise LOLSemanticError(f"Unknown boolean operator: '{op}'")

  return res


def eval_boolean_unary(node, scope, runtime):
  operand_val = evaluate_expression(node["operand"], scope, runtime)
  b = to_troof(operand_val)
  return not b

def values_equal(left_val, right_val):
  if typecast.COMPARE_NUMERIC_YARNS:
    if type_of(left_val) == "YARN" and yarn_to_number(left_val) is not None:
      left_val = yarn_to_number(left_val)
    if type_of(right_val) == "YARN" and yarn_to_number(right_val) is not None:
      right_val = yarn_to_number(right_val)

  if is_number(left_val) and is_number(right_val):
    return left_val == right_val
  elif type_of(left_val) != type_of(right_val):
    return False
  else:
    return left_val == right_val

def eval_comparison(node, scope, runtime):
  op = _get_op_lexeme(node["operator"])
  left_val = evaluate_expression(node["left"], scope, runtime)
  right_val = evaluate_expression(node["right"], scope, runtime)

  equal = values_equal(left_val, right_val)

  if op == "BOTH SAEM":
    return equal
  elif op == "DIFFRINT":
    return not equal
  else:
    raise LOLSemanticError(f"Unknown comparison operator: '{op}'")


def eval_concat(node, scope, runtime):
  # SMOOSH concatenates all operands after converting each to YARN
  parts = []
  for op_node in node["operands"]:
    val = evaluate_expression(op_node, scope, runtime)
    parts.append(to_yarn(val))
  return "".join(parts)


def eval_infinite_bool(node, scope, runtime):
  op = _get_op_lexeme(node["operator"])
  bool_values = []
  for op_node in node["operands"]:
    val = evaluate_expression(op_node, scope, runtime)
    bool_values.append(to_troof(val))

  if op == "ALL OF":
    res = all(bool_values)
  elif op == "ANY OF":
    res = any(bool_values)
  else:
    raise LOLSemanticError(f"Unknown infinite bool operator: '{op}'")

  return res


def eval_typecast(node, scope, runtime):
  val = evaluate_expression(node["operand"], scope, runtime)
  target_token = node["target_type"]
  target_type = _get_op_lexeme(target_token)
  return cast_explicit(val, target_type)
