from analyzers.syntax.helpers import peek, advance, error, expect, expect_class, parse_linebreak, not_written
from analyzers.syntax import expressions, statements

def parse_if_then(parser):
  # <if_then> ::= O RLY? <linebreak> <if_clause> <else_ifs> <else_clause> OIC
  not_written(parser, "parse_if_then")


def parse_if_clause(parser):
  # <if_clause> ::= YA RLY <linebreak> <code_block>
  not_written(parser, "parse_if_clause")


def parse_else_ifs(parser):
  # <else_ifs> ::= ε | MEBBE <expression> <linebreak> <code_block> <else_ifs>
  not_written(parser, "parse_else_ifs")


def parse_else_clause(parser):
  # <else_clause> ::= ε | NO WAI <linebreak> <code_block>
  not_written(parser, "parse_else_clause")


def parse_switch(parser):
  # <switch> ::= WTF? <linebreak> <cases> <default_case> OIC
  not_written(parser, "parse_switch")


def parse_cases(parser):
  # <cases> ::= <case> | <case> <cases>
  not_written(parser, "parse_cases")


def parse_case(parser):
  # <case> ::= OMG <literal> <linebreak> <code_block>
  not_written(parser, "parse_case")


def parse_default_case(parser):
  # <default_case> ::= ε | OMGWTF <linebreak> <code_block>
  not_written(parser, "parse_default_case")


def parse_loop(parser):
  # <loop> ::= IM IN YR loopidentifier <loop_op> YR varident <loop_cond>
  #            <linebreak> <code_block> IM OUTTA YR loopidentifier
  not_written(parser, "parse_loop")


def parse_loop_op(parser):
  # <loop_op> ::= UPPIN | NERFIN
  not_written(parser, "parse_loop_op")


def parse_loop_cond(parser):
  # <loop_cond> ::= ε | TIL <expression> | WILE <expression>
  not_written(parser, "parse_loop_cond")