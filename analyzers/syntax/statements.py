from analyzers.syntax.helpers import peek, advance, error, expect, expect_class, parse_linebreak, not_written
from analyzers.syntax import expressions, flow_control, functions

def parse_code_block(parser):
  # <code_block> ::= ε | <statement> <linebreak> <statements>
  # <statements> ::= <statement> <linebreak> <statements> | <statement> <linebreak>
  not_written(parser, "parse_code_block")

def parse_statement(parser):
  # <statement> ::= <print> | <input> | <assignment> | <expression> | <if_then>
  #               | <switch> | <loop> | <recast> | <func_def> | <func_return>
  #               | <break>
  not_written(parser, "parse_statement")


def parse_print(parser):
  # <print>      ::= VISIBLE <print_args>
  # <print_args> ::= <expression> | <expression> + <print_args>
  not_written(parser, "parse_print")


def parse_input(parser):
  # <input> ::= GIMMEH varident
  not_written(parser, "parse_input")


def parse_assignment(parser):
  # <assignment> ::= varident R <expression>
  not_written(parser, "parse_assignment")


def parse_recast(parser):
  # <recast> ::= varident IS NOW A type
  not_written(parser, "parse_recast")


def parse_break(parser):
  # <break> ::= GTFO
  not_written(parser, "parse_break")
