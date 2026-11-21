# ========================================== RUN LOL FILE ==========================================================

# type sa terminal: 
#   python run_lol.py <file path ng lol file>
#   ex: 
#   python run_lol.py test_lol/01_variables.lol 
#

import sys
from analyzers.lexical_analyzer import preprocess, tokenize, validation, check_comments
from analyzers.syntax_analyzer import parse
from analyzers.semantic_analyzer import run


def main():
  if len(sys.argv) < 2:
    print("usage: python run_lol.py <file.lol>")
    return

  code = open(sys.argv[1]).read()
  
  # 1. LEXICAL
  tokens = tokenize(preprocess(code))
  lexical_errors = check_comments(code) + validation(tokens)
  if lexical_errors:
    print("Lexical errors found:")
    print("\n".join(lexical_errors))
    return

  # 2. SYNTAX
  result = parse(tokens)
  if result["errors"]:
    print("Syntax errors found:")
    print("\n".join(result["errors"]))
    return

  # 3. SEMANTIC 
  answer = run(result["ast"])
  print(answer["output"], end="")
  for error in answer["errors"]:
    print(error)
  if answer["need_input"] is not None:
    print(f"(program stopped: GIMMEH {answer['need_input']} needs input, not supported here yet)")

  print("\n--- symbol table ---")
  for row in answer["symbols"]:
    print(f"{row['identifier']:<12} {row['value']:<20} {row['type']}")


if __name__ == "__main__":
  main()