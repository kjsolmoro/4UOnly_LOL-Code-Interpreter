from analyzers.syntax.helpers import peek, advance, error, expect, expect_class, parse_linebreak, not_written
from analyzers.syntax import expressions, statements


def parse_func_def(parser):
  # <func_def> ::= HOW IZ I func_identifier <params> <linebreak> <code_block> IF U SAY SO
  not_written(parser, "parse_func_def")


def parse_params(parser):
  # <params> ::= ε | <param_list>
  not_written(parser, "parse_params")


def parse_param_list(parser):
  # <param_list> ::= YR varident | YR varident AN <param_list>
  not_written(parser, "parse_param_list")


def parse_func_return(parser):
  # <func_return> ::= FOUND YR <expression>
  not_written(parser, "parse_func_return")


def parse_func_call(parser):
  # <func_call> ::= I IZ functionidentifier <args> MKAY
  not_written(parser, "parse_func_call")


def parse_args(parser):
  # <args> ::= ε | <args_list>
  not_written(parser, "parse_args")


def parse_args_list(parser):
  # <args_list> ::= YR <operand> | YR <operand> AN <args_list>
  not_written(parser, "parse_args_list")
