'''
  parser = {"tokens": [...], "position": 0}

  "tokens" : token[i][lexeme, classification, line_number], + Linebreak tokens
             **(nabura kasi mga '\n' sa lexer, kailangan ibalik kasi yung grammar natin may mga linebreak)
  position : index of token currently parsing

'''

class LOLSyntaxError(Exception):
  pass


def show(lexeme):
  # helper to print the lexeme in error messages
  if lexeme == "\n":
    return "end of line"
  return f"'{lexeme}'"


def add_linebreaks(tokens):
  # bring back the \n removed by lexer, add it as linebreak tokeb
  result = []
  for i in range(len(tokens)):
    result.append(tokens[i])
    is_last = (i == len(tokens) - 1)                 
    if is_last or tokens[i + 1][2] != tokens[i][2]:  # current token's line not same with next token's line, therefor there there's \n
      result.append(("\n", "Linebreak", tokens[i][2]))
  return result


def peek(parser):
  # see the current token that is being parsed
  if parser["position"] < len(parser["tokens"]):
    return parser["tokens"][parser["position"]]

  if parser["tokens"]:                      
    last_line = parser["tokens"][-1][2]      
  else:                                      
    last_line = 1
  return ("end of file", "EOF", last_line)  # incase end of file is reached but there is still token to be expected, extra token for expect() has someting to expect  


def advance(parser):
  # proceed to the next token to be parsed, returns the token we just parsed
  token = peek(parser)
  parser["position"] += 1
  return token


def error(parser, message):
  # stop parsing and report error
  lexeme, classification, line = peek(parser)
  raise LOLSyntaxError(f"Line {line}: {message}, but found {show(lexeme)}")


def expect(parser, lexeme):
  # see if the next expected token follows the grammar. error() if expected token is not met, advance() if the expected is satisfied
  if peek(parser)[0] != lexeme:
    error(parser, f"expected '{lexeme}'")
  return advance(parser)


def expect_class(parser, classification, description):
  # see if the next expected kind of token follows the grammar. error() if expected token is not met, advance() if the expected is satisfied
  if peek(parser)[1] != classification:
    error(parser, f"expected {description}")
  return advance(parser)


def parse_linebreak(parser):
  # for end of line
  expect_class(parser, "Linebreak", "end of line")


def not_written(parser, name):
  # placeholder for functions that are not written yet
  lexeme, classification, line = peek(parser)
  raise LOLSyntaxError(f"Line {line}: {name} is not written yet")
