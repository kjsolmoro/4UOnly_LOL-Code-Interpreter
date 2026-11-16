from analyzers.syntax.helpers import peek, advance, error, expect, expect_class, parse_linebreak, not_written
from analyzers.syntax import expressions, statements, functions


def parse_program(parser):
  # <program> ::= <comments> <functions> HAI <linebreak> <var_section>
  #               <code_block> KTHXBYE <linebreak> <functions>
  pre_funcs = parse_functions(parser)
  expect(parser, "HAI")
  parse_linebreak(parser)
  declarations = parse_var_section(parser)
  body = statements.parse_code_block(parser)
  expect(parser, "KTHXBYE")
  parse_linebreak(parser)
  post_funcs = parse_functions(parser)

  if peek(parser)[1] != "EOF":
    error(parser, "expected end of file")

  return {
    "type": "program",
    "functions": pre_funcs + post_funcs,
    "declarations": declarations,
    "body": body,
  }


def parse_functions(parser):
  # <functions> ::= ε | <func_def> <linebreak> <functions>
  funcs = []
  while peek(parser)[0] == "HOW IZ I":
    funcs.append(functions.parse_func_def(parser))
    parse_linebreak(parser)
  return funcs


def parse_var_section(parser):
  # <var_section> ::= ε | WAZZUP <linebreak> <declarations> BUHBYE <linebreak>
  if peek(parser)[0] != "WAZZUP":
    return []
  expect(parser, "WAZZUP")
  parse_linebreak(parser)
  declarations = parse_declarations(parser)
  expect(parser, "BUHBYE")
  parse_linebreak(parser)
  return declarations


def parse_declarations(parser):
  # <declarations> ::= ε | <declaration> <linebreak> <declarations>
  declarations = []
  while peek(parser)[0] == "I HAS A":
    declarations.append(parse_declaration(parser))
    parse_linebreak(parser)
  return declarations


def parse_declaration(parser):
  # <declaration> ::= I HAS A varident | I HAS A varident <init>
  expect(parser, "I HAS A")
  name_token = expect_class(parser, "Variable Identifier", "a variable name")
  init = parse_init(parser)
  return {"type": "declare", "var": name_token[0], "init": init}

def parse_init(parser):
  # <init> ::= ε | ITZ <expression>
  if peek(parser)[0] == "ITZ":
    advance(parser)
    return expressions.parse_expression(parser)
  return None
