from analyzers.syntax.helpers import peek, advance, error, expect, expect_class, not_written
from analyzers.syntax import functions

def is_expression_start(parser):
  not_written(parser, "is_expression_start")

def parse_expression(parser):
  # <expression> ::= <operand> | <concat> | <infinite_bool>
  token = peek() 

  if token == "SMOOSH":
      return parse_concat()
  elif token in ["ALL OF", "ANY OF"]:
      return parse_infinite_bool()
  else: 
      return parse_operand()
  
def parse_operand(parser):
  # <operand> ::= varident | <literal> | <arithmetic> | <boolean>
  #             | <comparison> | <typecast> | <func_call>
  token = peek()

  if token in ["NUMBR", "NUMBAR", "YARN", "TROOF"]:
      return parse_literal()
  elif token == "varident":
      return consume("varident")

  elif token in ["SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", "MOD OF", "BIGGR OF", "SMALLR OF"]:
      return parse_arithmetic()

  elif token in ["BOTH OF", "EITHER OF", "WON OF", "NOT"]:
      return parse_boolean()

  elif token in ["BOTH SAEM", "DIFFRINT"]:
      return parse_comparison()

  elif token == "MAEK":
      return parse_typecast()

  elif token == "I IZ":
      pass 

  else: 
      raise SyntaxError(f"Expected an operand, but got {token}")

def parse_literal(parser):
  # <literal> ::= numbr | numbar | yarn | troof
  not_written(parser, "parse_literal")


def parse_arithmetic(parser):
  # <arithmetic> ::= <arith_op> <operand> AN <operand>
  not_written(parser, "parse_arithmetic")


def parse_arith_op(parser):
  # <arith_op> ::= SUM OF | DIFF OF | PRODUKT OF | QUOSHUNT OF | MOD OF
  #              | BIGGR OF | SMALLR OF
  not_written(parser, "parse_arith_op")


def parse_boolean(parser):
  # <boolean> ::= <bool_op> <operand> AN <operand> | NOT <operand>
  not_written(parser, "parse_boolean")


def parse_bool_op(parser):
  # <bool_op> ::= BOTH OF | EITHER OF | WON OF
  not_written(parser, "parse_bool_op")


def parse_comparison(parser):
  # <comparison> ::= <comp_op> <operand> AN <operand>
  not_written(parser, "parse_comparison")


def parse_comp_op(parser):
  # <comp_op> ::= BOTH SAEM | DIFFRINT
  not_written(parser, "parse_comp_op")


def parse_infinite_bool(parser):
  # <infinite_bool> ::= ALL OF <operand_list> MKAY | ANY OF <operand_list> MKAY
  not_written(parser, "parse_infinite_bool")


def parse_concat(parser):
  # <concat> ::= SMOOSH <operand_list>
  not_written(parser, "parse_concat")


def parse_operand_list(parser):
  # <operand_list> ::= <operand> AN <operand> | <operand> AN <operand_list>
  not_written(parser, "parse_operand_list")


def parse_typecast(parser):
  # <typecast> ::= MAEK <operand> A type | MAEK <operand> type
  not_written(parser, "parse_typecast")
