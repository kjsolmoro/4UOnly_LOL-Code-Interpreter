from analyzers.syntax.helpers import peek, advance, error, expect, expect_class, parse_linebreak, not_written
from analyzers.syntax import expressions, statements


def parse_func_def(parser):
  # <func_def> ::= HOW IZ I func_identifier <params> <linebreak> <code_block> IF U SAY SO
  expect(parser, "HOW IZ I")
  name_token = expect_class(parser, "Function Identifier", "a function name")
  params = parse_params(parser)
  parse_linebreak(parser)
  body = statements.parse_code_block(parser)
  expect(parser, "IF U SAY SO")
  return {"type": "func_def", "name": name_token[0], "params": params, "body": body}

def parse_params(parser):
  # <params> ::= ε | <param_list>
  if peek(parser)[0] == "YR":
    return parse_param_list(parser)
  return []



def parse_param_list(parser):
  # <param_list> ::= YR varident | YR varident AN YR varident
  params = []
  expect(parser, "YR")
  param_token = expect_class(parser, "Variable Identifier", "a parameter name")
  params.append(param_token[0])
  while peek(parser)[0] == "AN":
    advance(parser)
    expect(parser, "YR")
    param_token = expect_class(parser, "Variable Identifier", "a parameter name")
    params.append(param_token[0])
  return params


def parse_func_return(parser):
  # <func_return> ::= FOUND YR <expression>
  expect(parser, "FOUND YR")
  expr = expressions.parse_expression(parser)
  return {"type": "func_return", "expr": expr}


def parse_func_call(parser):
  # <func_call> ::= I IZ functionidentifier <args> MKAY
  expect(parser, "I IZ")
  name_token = expect_class(parser, "Function Identifier", "a function name")
  args = parse_args(parser)
  expect(parser, "MKAY")
  return {"type": "func_call", "name": name_token[0], "args": args}


def parse_args(parser):
  # <args> ::= ε | <args_list>
  if peek(parser)[0] == "YR":
    return parse_args_list(parser)
  return []


def parse_args_list(parser):
  # <args_list> ::= YR <operand> | YR <operand> AN YR <operand>
  args = []
  expect(parser, "YR")
  args.append(expressions.parse_operand(parser))
  while peek(parser)[0] == "AN":
    advance(parser)
    expect(parser, "YR")
    args.append(expressions.parse_operand(parser))
  return args
