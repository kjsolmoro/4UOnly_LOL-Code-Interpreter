from analyzers.syntax.helpers import peek, advance, error, expect, expect_class, not_written
from analyzers.syntax import functions

def is_expression_start(parser):

  if parser["position"] >= len(parser["tokens"]):
      return False
  
  token, classification, _ = peek(parser)

  valid_starts = [
     "SMOOSH", "ALL OF", "ANY OF",
     "NUMBR", "NUMBAR", "YARN", "TROOF", "varident",
     "SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", "MOD OF", "BIGGR OF", "SMALLR OF",
     "BOTH OF", "EITHER OF", "WON OF", "NOT",
      "BOTH SAEM", "DIFFRINT",
      "MAEK", "I IZ"
    ]
  
  return token in valid_starts or classification in ["NUMBR Literal", "NUMBAR Literal", "YARN Literal", "TROOF Literal", "Variable Identifier"]

def parse_expression(parser):
  # <expression> ::= <operand> | <concat> | <infinite_bool>
  token, classification, _ = peek(parser)

  if token == "SMOOSH":
      return parse_concat(parser)
  elif token in ["ALL OF", "ANY OF"]:
      return parse_infinite_bool(parser)
  else: 
      return parse_operand(parser)
  
def parse_operand(parser):
  # <operand> ::= varident | <literal> | <arithmetic> | <boolean>
  #             | <comparison> | <typecast> | <func_call>
  token, classification, _ = peek(parser)

  if classification in ["NUMBR Literal", "NUMBAR Literal", "YARN Literal", "TROOF Literal"]:
      return parse_literal(parser)
  elif classification == "Variable Identifier":
      return advance(parser)

  elif token in ["SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", "MOD OF", "BIGGR OF", "SMALLR OF"]:
      return parse_arithmetic(parser)

  elif token in ["BOTH OF", "EITHER OF", "WON OF", "NOT"]:
      return parse_boolean(parser)

  elif token in ["BOTH SAEM", "DIFFRINT"]:
      return parse_comparison(parser)

  elif token == "MAEK":
      return parse_typecast(parser)

  elif token == "I IZ":
      pass 

  else: 
      if token == "\n":
          error(parser, "Expected an operand")
      else:
          error(parser, f"Expected an operand")

def parse_literal(parser):
  # <literal> ::= numbr | numbar | yarn | troof
  
  # dinagdag ko langs for error handling
  if peek(parser)[1] not in ["NUMBR Literal", "NUMBAR Literal", "YARN Literal", "TROOF Literal"]:
    error(parser, "expected a literal")
  return advance(parser)
  
def parse_arithmetic(parser):
  # <arithmetic> ::= <arith_op> <operand> AN <operand>
  op = parse_arith_op(parser)
  left = parse_operand(parser)
  expect(parser, "AN")
  right = parse_operand(parser)
  return {"type": "arithmetic", "op": op, "left": left, "right": right}


def parse_arith_op(parser):
  # <arith_op> ::= SUM OF | DIFF OF | PRODUKT OF | QUOSHUNT OF | MOD OF
  #              | BIGGR OF | SMALLR OF
  token, _, _ = peek(parser)
  if token in ["SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", "MOD OF", "BIGGR OF", "SMALLR OF"]:
       return advance(parser)
  error(parser, f"Expected arithmetic operator, got: {token}")


def parse_boolean(parser):
  # <boolean> ::= <bool_op> <operand> AN <operand> | NOT <operand>
  token, _, _ = peek(parser)
  if token == "NOT": 
     op = advance(parser)
     operand = parse_operand(parser)
     return {"type": "boolean_unary", "operator": op, "operand": operand}
  else:
      op = parse_bool_op(parser)
      left = parse_operand(parser)
      expect(parser, "AN")
      right = parse_operand(parser)
      return {"type": "boolean_binary", "operator": op, "left": left, "right": right}



def parse_bool_op(parser):
  # <bool_op> ::= BOTH OF | EITHER OF | WON OF
  token, _, _ = peek(parser)
  if token in ["BOTH OF", "EITHER OF", "WON OF"]: 
     return advance(parser)
  error(parser, f"Expected boolean operator, got: {token}")


def parse_comparison(parser):
  # <comparison> ::= <comp_op> <operand> AN <operand>
  op = parse_comp_op(parser)
  left = parse_operand(parser)
  expect(parser, "AN")
  right = parse_operand(parser)
  return {"type": "comparison", "operator": op, "left": left, "right": right}


def parse_comp_op(parser):
  # <comp_op> ::= BOTH SAEM | DIFFRINT
  token, _, _ = peek(parser)
  if token in ["BOTH SAEM", "DIFFRINT"]:
      return advance(parser)
  error(parser, f"Expected comparison operator, got: {token}")


def parse_infinite_bool(parser):
  # <infinite_bool> ::= ALL OF <operand_list> MKAY | ANY OF <operand_list> MKAY
  op = advance(parser)
  operands = parse_operand_list(parser)
  expect(parser, "MKAY")
  return {"type": "infinite_bool", "operator": op, "operands": operands}


def parse_concat(parser):
  # <concat> ::= SMOOSH <operand_list>
  expect(parser, "SMOOSH")
  operands = parse_operand_list(parser)
  return {"type": "concat", "operands": operands}


def parse_operand_list(parser):
  # <operand_list> ::= <operand> AN <operand> | <operand> AN <operand_list>
  operands = []

  operands.append(parse_operand(parser))

  while parser["position"] < len(parser["tokens"]):
    token, _, _ = peek(parser)
    if token != "AN":
      break
    expect(parser, "AN")
    operands.append(parse_operand(parser))

  return operands

def parse_typecast(parser):
  # <typecast> ::= MAEK <operand> A type | MAEK <operand> type
  expect(parser, "MAEK")
  operand = parse_operand(parser)

  token, _, _ = peek(parser)
  if token == "A":
       expect(parser, "A")
        
  target_type = advance(parser) 
  return {"type": "typecast", "operand": operand, "target_type": target_type}
