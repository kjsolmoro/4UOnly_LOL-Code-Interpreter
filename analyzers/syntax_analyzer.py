#(OwO)==================================================================
# SYNTAX ANALYZER (Milestone 2 -> Milestone 3 AST output)
#(OwO)==================================================================
'''
Input : the token list from lexical_analyzer.tokenize()
        -> list of (lexeme, classification, line_number)
Output: {"ast": <program_node> | None, "errors": [str]}

The parser builds an AST made of dictionaries.
'''

from analyzers.syntax.helpers import add_linebreaks, LOLSyntaxError
from analyzers.syntax.program import parse_program

# tokens from the lexical analyzer (U-U)
# symbols : list of dictionaries that the parser would fill for the symbol table (O-O)
#     [{symbol, value}, {symbol, value} ... ]
def parse(tokens):
  parser = {"tokens": add_linebreaks(tokens), "position": 0}
  try:
    ast = parse_program(parser)
    return {"ast": ast, "errors": []}
  except LOLSyntaxError as e:
    return {"ast": None, "errors": [str(e)]}
