from analyzers.syntax.helpers import peek, peek_next, advance, error, expect, expect_class, parse_linebreak, not_written
from analyzers.syntax import expressions, flow_control, functions

def parse_code_block(parser):
  # <code_block> ::= ε | <statement> <linebreak> <code_block>
  while not is_block_end(parser):       # is_block_end() ->helper function, nasa baba docs
    parse_statement(parser)
    parse_linebreak(parser)
    

def parse_statement(parser):
  # <statement> ::= <print> | <input> | <assignment> | <expression> | <if_then>
  #               | <switch> | <loop> | <recast> | <func_def> | <func_return>
  #               | <break>
  lexeme, classification, line = peek(parser)

  if lexeme == "VISIBLE":
    parse_print(parser)
  elif lexeme == "GIMMEH":
    parse_input(parser)
  elif lexeme == "GTFO":
    parse_break(parser)
  elif lexeme == "O RLY?":
    flow_control.parse_if_then(parser)
  elif lexeme == "WTF?":
    flow_control.parse_switch(parser)
  elif lexeme == "IM IN YR":
    flow_control.parse_loop(parser)
  elif lexeme == "HOW IZ I":
    functions.parse_func_def(parser)
  elif lexeme == "FOUND YR":
    functions.parse_func_return(parser)
  
  # **Statements that START WITH A VARIABLE
  #   A variable can begin 3 diff statements:
  #     x R 5             -> assignment   (2nd token is R)
  #     x IS NOW A YARN   -> recast       (2nd token is IS NOW A)
  #     x                 -> expression   (anything else, handled below)
  #   Pansinin nyo yung 1st token (x) same in all 3, gumamit ako peek_next() para makita ung 2nd token, saka ako nagdecide kung saan grammar sya papasok
  
  elif classification == "Variable Identifier" and peek_next(parser)[0] == "R":
    parse_assignment(parser)
  elif classification == "Variable Identifier" and peek_next(parser)[0] == "IS NOW A":
    parse_recast(parser)
  elif expressions.is_expression_start(parser):
    expressions.parse_expression(parser)

  else:
    error(parser, "expected a statement")


def parse_print(parser):
  # <print> ::= VISIBLE <print_args>
  expect(parser, "VISIBLE")
  parse_print_args(parser)


def parse_print_args(parser):
  # <print_args> ::= <expression> | <expression> + <print_args>
  expressions.parse_expression(parser)          # <expression>
  while peek(parser)[0] == "+":                 # continuesly check if the token to be parsed still has "+" (since expression can be chained with +)
    advance(parser)                             # proceed to the next token to be parsed (since you are currently in "+")
    expressions.parse_expression(parser)        # then the next <expression> 


def parse_input(parser):
  # <input> ::= GIMMEH varident
  expect(parser, "GIMMEH")
  expect_class(parser, "Variable Identifier", "a variable")


def parse_assignment(parser):
  # <assignment> ::= varident R <expression>
  expect_class(parser, "Variable Identifier", "a variable name")
  expect(parser, "R")
  expressions.parse_expression(parser)


def parse_recast(parser):
  # <recast> ::= varident IS NOW A type
  expect_class(parser, "Variable Identifier", "a variable name")
  expect(parser, "IS NOW A")
  expect_class(parser, "TYPE Literal", "a type (NUMBR, NUMBAR, YARN, TROOF, NOOB)")


def parse_break(parser):
  # <break> ::= GTFO
  expect(parser, "GTFO")


# ======================= HELPER FUNCTIONS ==============================
BLOCK_ENDS = [
  "KTHXBYE",                    # end of program
  "OIC",                        # end of if-then / switch
  "MEBBE", "NO WAI",            # next part of if-then
  "OMG", "OMGWTF",              # next case of switch
  "IM OUTTA YR",                # end of loop
  "IF U SAY SO",                # end of function
]

'''
  Sa grammar kasi natin, yung <code_block> = basically group of statements, diba?
  Pwede siya maging part ng program, if-else, switch, loop, function, etc.
  (ctrl+f niyo na lang yung <code_block> sa Proj Req 2 if di niyo gets)

  Ang problema: since pwede siya magamit in many places, alam natin kung saan
  siya nag-start (sa first statement), pero hindi natin alam kung saan siya
  mag-eend o hanggang saan yung scope niya.

  Solution: BLOCK_ENDS = list ng mga "stop words"
  - Yung code block, babasahin lang niya yung statements line by line.
  - Pag nakita niya yung isa sa mga stop words (KTHXBYE, OIC, NO WAI, etc.),
    titigil na siya, kasi ibig sabihin tapos na yung block.
  - Hindi siya yung kukuha ng stop word. Titigil lang siya sa harap nito.
    Yung function na nag-open ng block yung mag-cha-check nun.

  Example:
    O RLY?
      YA RLY
        VISIBLE "pass"     <- code block ni YA RLY
        GIMMEH x           <- code block ni YA RLY
      NO WAI               <- STOP WORD! tapos na yung block ni YA RLY
        VISIBLE "fail"     <- code block ni NO WAI
    OIC                    <- STOP WORD! tapos na yung block ni NO WAI

  Kaya:
    parse_program  -> code block hihinto sa KTHXBYE      -> si parse_program mag-eexpect ng KTHXBYE
    parse_loop     -> code block hihinto sa IM OUTTA YR  -> si parse_loop mag-eexpect ng IM OUTTA YR
    parse_if_then  -> code block hihinto sa NO WAI / OIC -> si parse_if_then bahala dun

  Kasama rin yung EOF (wala nang tokens) para kung nakalimutan yung KTHXBYE,
  hindi mag-loop forever. Hihinto lang siya, tapos error na "expected KTHXBYE".
'''
def is_block_end(parser):
  lexeme, classification, line = peek(parser)
  
  if lexeme in BLOCK_ENDS:          # a keyword like OIC, KTHXBYE, etcc
    return True
  if classification == "EOF":       # no more tokens at all
    return True
  return False
