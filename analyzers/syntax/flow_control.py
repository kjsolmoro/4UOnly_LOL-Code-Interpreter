from analyzers.syntax.helpers import peek, advance, error, expect, expect_class, parse_linebreak, not_written
from analyzers.syntax import expressions, statements

def parse_if_then(parser):
  # <if_then> ::= O RLY? <linebreak> <if_clause> <else_ifs> <else_clause> OIC

  expect(parser, "O RLY?")
  parse_linebreak(parser)

  parse_if_clause(parser)
  parse_else_ifs(parser)
  parse_else_clause(parser)

  expect(parser, "OIC")


def parse_if_clause(parser):
  # <if_clause> ::= YA RLY <linebreak> <code_block>

  expect(parser, "YA RLY")
  parse_linebreak(parser)
  statements.parse_code_block(parser)


def parse_else_ifs(parser):
  # <else_ifs> ::= ε | MEBBE <expression> <linebreak> <code_block> <else_ifs>

  while peek(parser)[0] == "MEBBE": #handles reccursion nung <else_ifs>
    advance(parser)
    expressions.parse_expression(parser)
    parse_linebreak(parser)
    statements.parse_code_block(parser)


def parse_else_clause(parser):
  # <else_clause> ::= ε | NO WAI <linebreak> <code_block>

  if peek(parser)[0] == "NO WAI": #uses if for ε cases
    advance(parser)
    parse_linebreak(parser)
    statements.parse_code_block(parser)

# =======================================================================================================

def parse_switch(parser):
  # <switch> ::= WTF? <linebreak> <cases> <default_case> OIC
  expect(parser, "WTF?")
  parse_linebreak(parser)

  parse_cases(parser)
  parse_default_case(parser)

  expect(parser, "OIC")


def parse_cases(parser):
  # <cases> ::= <case> | <case> <cases>
  parse_case(parser)

  while peek(parser)[0] == "OMG":
    parse_case(parser)


def parse_case(parser):
  # <case> ::= OMG <literal> <linebreak> <code_block>
  expect(parser, "OMG")
  expressions.parse_literal(parser)
  parse_linebreak(parser)
  statements.parse_code_block(parser)


def parse_default_case(parser):
  # <default_case> ::= ε | OMGWTF <linebreak> <code_block>
  if peek(parser)[0] == "OMGWTF": #uses if for ε cases 
    advance(parser)
    parse_linebreak(parser)
    statements.parse_code_block(parser)

# =======================================================================================================

def parse_loop(parser):
  # <loop> ::= IM IN YR loopidentifier <loop_op> YR varident <loop_cond>
  #            <linebreak> <code_block> IM OUTTA YR loopidentifier

  expect(parser, "IM IN YR")
  opening_loop_ident = expect_class(parser, "Loop Identifier", "a loop name")
  parse_loop_op(parser)
  expect(parser, "YR")
  expect_class(parser, "Variable Identifier", "a variable name")
  parse_loop_cond(parser)
  parse_linebreak(parser)
  statements.parse_code_block(parser)
  expect(parser, "IM OUTTA YR")
  closing_loop_ident = expect_class(parser, "Loop Identifier", "a loop name")

  # pang check if opening loopIdentifier matches with closing loopIdentifier 
  if closing_loop_ident[0] != opening_loop_ident[0]:
    error(parser, f"expected loop name '{opening_loop_ident[0]}'")


def parse_loop_op(parser):
  # <loop_op> ::= UPPIN | NERFIN

  token, _, _ = peek(parser)
  if token in ["UPPIN", "NERFIN"]:
    return advance(parser)

  error(parser, f"Expected a loop operator, got: {token}")


def parse_loop_cond(parser):
  # <loop_cond> ::= ε | TIL <expression> | WILE <expression>
  token, _, _ = peek(parser)

  if token in ["TIL", "WILE"]:
    advance(parser)
    expressions.parse_expression(parser)


# CHECK MO AFTER DINNER BAKS