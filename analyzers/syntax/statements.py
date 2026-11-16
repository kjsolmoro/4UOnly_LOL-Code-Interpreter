#(OwO)==================================================================
# STATEMENT-LEVEL GRAMMAR
#(OwO)==================================================================
from analyzers.syntax.helpers import peek, peek_next, advance, error, expect, expect_class, parse_linebreak
from analyzers.syntax import expressions, flow_control, functions


def parse_code_block(parser):
  # <code_block> ::= ε | <statement> <linebreak> <code_block>
  stmts = []
  while not is_block_end(parser):
    stmts.append(parse_statement(parser))
    parse_linebreak(parser)
  return stmts


def parse_statement(parser):
  # <statement> ::= <print> | <input> | <assignment> | <expression> | <if_then>
  #               | <switch> | <loop> | <recast> | <func_def> | <func_return>
  #               | <break>
  lexeme, classification, line = peek(parser)

  if lexeme == "VISIBLE":
    return parse_print(parser)
  elif lexeme == "GIMMEH":
    return parse_input(parser)
  elif lexeme == "GTFO":
    return parse_break(parser)
  elif lexeme == "O RLY?":
    return flow_control.parse_if_then(parser)
  elif lexeme == "WTF?":
    return flow_control.parse_switch(parser)
  elif lexeme == "IM IN YR":
    return flow_control.parse_loop(parser)
  elif lexeme == "HOW IZ I":
    return functions.parse_func_def(parser)
  elif lexeme == "FOUND YR":
    return functions.parse_func_return(parser)

  elif classification == "Variable Identifier" and peek_next(parser)[0] == "R":
    return parse_assignment(parser)
  elif classification == "Variable Identifier" and peek_next(parser)[0] == "IS NOW A":
    return parse_recast(parser)
  elif expressions.is_expression_start(parser):
    expr = expressions.parse_expression(parser)
    return {"type": "expression", "expr": expr}

  else:
    error(parser, "expected a statement")


def parse_print(parser):
  # <print> ::= VISIBLE <print_args>
  expect(parser, "VISIBLE")
  args = parse_print_args(parser)
  return {"type": "print", "args": args}


def parse_print_args(parser):
  # <print_args> ::= <expression> | <expression> + <print_args>
  args = []
  args.append(expressions.parse_expression(parser))
  while peek(parser)[0] == "+":
    advance(parser)
    args.append(expressions.parse_expression(parser))
  return args


def parse_input(parser):
  # <input> ::= GIMMEH varident
  expect(parser, "GIMMEH")
  var_token = expect_class(parser, "Variable Identifier", "a variable")
  return {"type": "input", "var": var_token[0]}


def parse_assignment(parser):
  # <assignment> ::= varident R <expression>
  var_token = expect_class(parser, "Variable Identifier", "a variable name")
  expect(parser, "R")
  expr = expressions.parse_expression(parser)
  return {"type": "assign", "var": var_token[0], "expr": expr}


def parse_recast(parser):
  # <recast> ::= varident IS NOW A type
  var_token = expect_class(parser, "Variable Identifier", "a variable name")
  expect(parser, "IS NOW A")
  type_token = expect_class(parser, "TYPE Literal", "a type (NUMBR, NUMBAR, YARN, TROOF, NOOB)")
  return {"type": "recast", "var": var_token[0], "target_type": type_token[0]}


def parse_break(parser):
  # <break> ::= GTFO
  expect(parser, "GTFO")
  return {"type": "break"}


# ======================= HELPER FUNCTIONS ==============================
BLOCK_ENDS = [
  "KTHXBYE",                    # end of program
  "OIC",                        # end of if-then / switch
  "MEBBE", "NO WAI",            # next part of if-then
  "OMG", "OMGWTF",              # next case of switch
  "IM OUTTA YR",                # end of loop
  "IF U SAY SO",                # end of function
]


def is_block_end(parser):
  lexeme, classification, line = peek(parser)
  if lexeme in BLOCK_ENDS:
    return True
  if classification == "EOF":
    return True
  return False
