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