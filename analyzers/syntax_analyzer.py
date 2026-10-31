#(OwO)==================================================================
# SYNTAX ANALYZER (Milestone 2)
#(OwO)==================================================================
'''
Input : the token list from lexical_analyzer.tokenize()
        -> list of (lexeme, classification, line_number)
Output: to be decided (parse result / syntax error messages)
'''

from analyzers.syntax.helpers import add_linebreaks, LOLSyntaxError
from analyzers.syntax.program import parse_program

# tokens from the lexical analyzer (U-U)
# symbols : list of dictionaries that the parser would fill for the symbol table (O-O)
#     [{symbol, value}, {symbol, value} ... ]
def parse(tokens, symbols=None): 
  if symbols is None: # default case only
    symbols = []
  parser = {"tokens": add_linebreaks(tokens), "position": 0, "symbols": symbols}
  try:
    parse_program(parser)
    return []
  except LOLSyntaxError as e:
    return [str(e)]
