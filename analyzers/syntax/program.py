from analyzers.syntax.helpers import peek, advance, error, expect, expect_class, parse_linebreak, not_written
from analyzers.syntax import expressions, statements, functions


def parse_program(parser):
  # <program> ::= <comments> <functions> HAI <linebreak> <var_section>
  #               <code_block> KTHXBYE <linebreak> <functions>
  # (<comments> is already removed by the lexer)
  not_written(parser, "parse_program")


def parse_functions(parser):
  # <functions> ::= ε | <func_def> <linebreak> <functions>
  # may be EMPTY (ε): if the next token doesn't start it, do nothing
  # LIST RULE: repeat with a while loop, NOT by calling this function again
  not_written(parser, "parse_functions")


def parse_var_section(parser):
  # <var_section> ::= ε | WAZZUP <linebreak> <declarations> BUHBYE <linebreak>
  # may be EMPTY (ε): if the next token doesn't start it, do nothing
  not_written(parser, "parse_var_section")


def parse_declarations(parser):
  # <declarations> ::= ε | <declaration> <linebreak> <declarations>
  # may be EMPTY (ε): if the next token doesn't start it, do nothing
  # LIST RULE: repeat with a while loop, NOT by calling this function again
  not_written(parser, "parse_declarations")


def parse_declaration(parser):
  # <declaration> ::= I HAS A varident | I HAS A varident <init>
  not_written(parser, "parse_declaration")


def parse_init(parser):
  # <init> ::= ε | ITZ <expression>
  # may be EMPTY (ε): if the next token doesn't start it, do nothing
  not_written(parser, "parse_init")
