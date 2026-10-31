#(OwO)==================================================================
# FLASK APP 
#(OwO)==================================================================
import sys
import io
from flask import Flask, jsonify, request, render_template

from analyzers.lexical_analyzer import preprocess, tokenize, validation, check_comments
from analyzers.syntax_analyzer import parse   # Milestone 2

HOST = '127.0.0.1'
PORT = 5000     # ngrok http 5000

app = Flask(__name__)

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/run', methods=['POST'])
def run():
  data = request.get_json()
  code = data.get("code", "")

  # (IoI) preprocess -> tokenize -> validation
  comment_errors = check_comments(code)
  cleaned = preprocess(code)
  tokens = tokenize(cleaned)

  # # Validation: returns a list of lexical errors
  # lexical_errors = comment_errors + validation(tokens)
  # syntax_errors = []
  # if tokens and not lexical_errors:
  #   syntax_errors = parse(tokens)

  # (3_3) list of tokens
  token_list = []
  for lexeme, classification, line in tokens:
    token_list.append({"lexeme": lexeme, "classification": classification, "line": line})

  # (4o4) symbol table 
  lexical_errors = comment_errors + validation(tokens)
  syntax_errors = []
  symbol_list = []
  # (PoP) If tokens exist, place an implicit IT variable but with NOOB val for now
  if tokens:
    symbol_list.append({"identifier": "IT", "value": "NOOB"})
  # (Y-Y) Then we go to second checking if it goes thru w/o lexical errors, now checking for syntax errors which
  #       is checked thru parse recursively and the stuff are appended to the symbol list as parse goes on
  # Table stays empty if there is a lexical error kc we skipped the parsing 
  if tokens and not lexical_errors:
    syntax_errors = parse(tokens, symbol_list)

  # (5-5) console text (KoK)
  if len(tokens) == 0:
    console_text = "Nothing to analyze (>n<)"
  else:
    console_text = "Lexical analysis finished: " + str(len(tokens)) + " lexemes found! (UwU)\n"
    console_text += "Lexical errors found: " + str(len(lexical_errors))
    if lexical_errors:
      console_text += "\n\n" + "\n".join(lexical_errors)
      console_text += "\n\nSyntax analysis skipped: fix the lexical errors first."
    elif syntax_errors:
      console_text += "\n\nSyntax analysis: errors found\n" + "\n".join(syntax_errors)
    else:
      console_text += "\n\nSyntax analysis finished: no syntax errors!"

  return jsonify({
      "tokens": token_list,
      "symbols": symbol_list,
      "errors": len(lexical_errors) + len(syntax_errors),
      "console": console_text,
  })

def run_app():
  app.run(host=HOST, port=PORT)

if __name__ == "__main__":
  run_app()
