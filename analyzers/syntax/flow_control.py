from analyzers.syntax.helpers import peek, advance, error, expect, expect_class, parse_linebreak, not_written
from analyzers.syntax import expressions, statements

def parse_if_then(parser):
  # <if_then> ::= O RLY? <linebreak> <if_clause> <else_ifs> <else_clause> OIC

  expect(parser, "O RLY?")
  parse_linebreak(parser)

  ya_rly = parse_if_clause(parser)
  mebbes = parse_else_ifs(parser)
  no_wai = parse_else_clause(parser)

  expect(parser, "OIC")

  return {"type": "if_then", "ya_rly": ya_rly, "mebbes": mebbes, "no_wai": no_wai}

def parse_if_clause(parser):
  # <if_clause> ::= YA RLY <linebreak> <code_block>

  expect(parser, "YA RLY")
  parse_linebreak(parser)
  return statements.parse_code_block(parser)


def parse_else_ifs(parser):
  # <else_ifs> ::= ε | MEBBE <expression> <linebreak> <code_block> <else_ifs>
  mebbes = []
  while peek(parser)[0] == "MEBBE":
    advance(parser)
    condition = expressions.parse_expression(parser)
    parse_linebreak(parser)
    body = statements.parse_code_block(parser)
    mebbes.append({"condition": condition, "body": body})
  return mebbes


def parse_else_clause(parser):
  # <else_clause> ::= ε | NO WAI <linebreak> <code_block>
  if peek(parser)[0] == "NO WAI":
    advance(parser)
    parse_linebreak(parser)
    return statements.parse_code_block(parser)
  return None

# =======================================================================================================

def parse_switch(parser):
  # <switch> ::= WTF? <linebreak> <cases> <default_case> OIC
  expect(parser, "WTF?")
  parse_linebreak(parser)

  cases = parse_cases(parser)
  default = parse_default_case(parser)

  expect(parser, "OIC")

  return {"type": "switch", "cases": cases, "default": default}

def parse_cases(parser):
  # <cases> ::= <case> | <case> <cases>
  cases = []
  cases.append(parse_case(parser))
  while peek(parser)[0] == "OMG":
    cases.append(parse_case(parser))
  return cases


def parse_case(parser):
  # <case> ::= OMG <literal> <linebreak> <code_block>
  expect(parser, "OMG")
  literal = expressions.parse_literal(parser)
  parse_linebreak(parser)
  body = statements.parse_code_block(parser)
  return {"value": literal, "body": body}


def parse_default_case(parser):
  # <default_case> ::= ε | OMGWTF <linebreak> <code_block>
  if peek(parser)[0] == "OMGWTF":
    advance(parser)
    parse_linebreak(parser)
    return statements.parse_code_block(parser)
  return None

# =======================================================================================================

def parse_loop(parser):
  # <loop> ::= IM IN YR loopidentifier <loop_op> YR varident <loop_cond>
  #            <linebreak> <code_block> IM OUTTA YR loopidentifier

  expect(parser, "IM IN YR")
  opening_label = expect_class(parser, "Loop Identifier", "a loop name")
  op = parse_loop_op(parser)
  expect(parser, "YR")
  var_token = expect_class(parser, "Variable Identifier", "a variable name")
  cond = parse_loop_cond(parser)
  parse_linebreak(parser)
  body = statements.parse_code_block(parser)
  expect(parser, "IM OUTTA YR")
  closing_label = expect_class(parser, "Loop Identifier", "a loop name")

  if closing_label[0] != opening_label[0]:
    error(parser, f"expected loop name '{opening_label[0]}'")

  return {
    "type": "loop",
    "label": opening_label[0],
    "op": op[0],
    "var": var_token[0],
    "cond": cond,
    "body": body,
  }

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
    kind_token = advance(parser)
    expr = expressions.parse_expression(parser)
    return {"kind": kind_token[0], "expr": expr}
  return None
