from analyzers.syntax.helpers import peek, advance, error, expect, expect_class, parse_linebreak, not_written
from analyzers.syntax import expressions, statements


def parse_func_def(parser):
  # <func_def> ::= HOW IZ I func_identifier <params> <linebreak> <code_block> IF U SAY SO
  expect(parser, "HOW IZ I")
  expect_class(parser, "Function Identifier", "a function name")
  parse_params(parser)
  parse_linebreak(parser)
  statements.parse_code_block(parser)
  expect(parser, "IF U SAY SO")

def parse_params(parser):
  # <params> ::= ε | <param_list>
  if peek(parser)[0] == "YR":       # i used if since it could be ε
    parse_param_list(parser)



def parse_param_list(parser):
  # <param_list> ::= YR varident | YR varident AN <param_list>
  expect(parser, "YR")
  expect_class(parser, "Variable Identifier", "a parameter name")
  while peek(parser)[0] == "AN":
    advance(parser)
    expect(parser,"YR")
    expect_class(parser, "Variable Identifier", "a parameter name")


def parse_func_return(parser):
  # <func_return> ::= FOUND YR <expression>
  expect(parser, "FOUND YR")
  expressions.parse_expression(parser)


def parse_func_call(parser):
  # <func_call> ::= I IZ functionidentifier <args> MKAY
  expect(parser, "I IZ")
  expect_class(parser, "Function Identifier", "a function name")
  parse_args(parser)
  expect(parser, "MKAY")

def parse_args(parser):
  # <args> ::= ε | <args_list>
  if peek(parser)[0] == "YR":
    parse_args_list(parser)


def parse_args_list(parser):
  # <args_list> ::= YR <operand> | YR <operand> AN <args_list>
  expect(parser, "YR")
  expressions.parse_operand(parser)
  while peek(parser)[0] == "AN":
    advance(parser)
    expect(parser, "YR")
    expressions.parse_operand(parser)
