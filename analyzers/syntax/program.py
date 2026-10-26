from analyzers.syntax.helpers import peek, advance, error, expect, expect_class, parse_linebreak, not_written
from analyzers.syntax import expressions, statements, functions


def parse_program(parser):
  # <program> ::= <comments> <functions> HAI <linebreak> <var_section>
  #               <code_block> KTHXBYE <linebreak> <functions>
  # (<comments> is already removed by the lexer)
  parse_functions(parser) 
  expect(parser, "HAI")
  parse_linebreak(parser)
  parse_var_section(parser)
  statements.parse_code_block(parser)
  expect(parser, "KTHXBYE")
  parse_linebreak(parser)
  parse_functions(parser)

  if peek(parser)[1] != "EOF":
    error(parser, "expected end of file")


def parse_functions(parser):
  # <functions> ::= ε | <func_def> <linebreak> <functions>
  while peek(parser)[0] == "HOW IZ I":
    functions.parse_func_def(parser)
    parse_linebreak(parser)


def parse_var_section(parser):
  # <var_section> ::= ε | WAZZUP <linebreak> <declarations> BUHBYE <linebreak>
  if peek(parser)[0] != "WAZZUP":
    return
  expect(parser, "WAZZUP")
  parse_linebreak(parser)
  parse_declarations(parser)    
  expect(parser, "BUHBYE")
  parse_linebreak(parser)


def parse_declarations(parser):
  # <declarations> ::= ε | <declaration> <linebreak> <declarations>
  while peek(parser)[0] == "I HAS A":
    parse_declaration(parser)
    parse_linebreak(parser)


def parse_declaration(parser):
  # <declaration> ::= I HAS A varident | I HAS A varident <init>
  expect(parser, "I HAS A")
  expect_class(parser, "Variable Identifier", "a variable name")
  parse_init(parser)

def parse_init(parser):
  # <init> ::= ε | ITZ <expression>
  if peek(parser)[0] == "ITZ":
    advance(parser)
    expressions.parse_expression(parser)
