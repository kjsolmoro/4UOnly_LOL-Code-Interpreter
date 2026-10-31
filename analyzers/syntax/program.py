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
  name = expect_class(parser, "Variable Identifier", "a variable name")
  init = parse_init(parser)
  add_symbol(parser, name, init)

def parse_init(parser):
  # <init> ::= ε | ITZ <expression>
  if peek(parser)[0] == "ITZ":
    advance(parser)
    return expressions.parse_expression(parser)
  return None

# (UwU) ========================================================================================
# NEW Add Symbol function
# Checks the tokens, set the value based on parse_expression returns, append to the symbol list
# (UwU) ========================================================================================
def add_symbol(parser, name_token, init):
  value = "NOOB"
  if init is None:                                  # no ITZ
    value = "NOOB"
  elif type(init) == dict:                          # SUM OF, SMOOSH, etc., 
    value = "(expression)"                          # mag eevaluate ng expressions eh so I think milestone 3 na siya?
  elif init[1] == "Variable Identifier":            # I HAS A x ITZ y
    value = find_symbol_value(parser, init[0])
  else:
    value = init[0]
  parser["symbols"].append({"identifier": name_token[0], "value": value})

# helper! find symbol value
# for already declared variables
# I HAS A num ITZ 17
# I HAS  copy ITZ num <-- finds num's value and places it in copy!
def find_symbol_value(parser, name):
  for symbol in parser["symbols"]:
    if symbol["identifier"] == name:
      return symbol["value"]
  return "NOOB"                       # fallback for when var is never declared 
                                      # for bext milestone na ren ata e2? since syntax plng nmn