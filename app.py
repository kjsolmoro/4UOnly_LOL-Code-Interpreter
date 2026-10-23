#(OwO)==================================================================
# FLASK APP 
#(OwO)==================================================================
import sys
import io
from flask import Flask, jsonify, request, render_template

from analyzers.lexical_analyzer import preprocess, tokenize, validation
# from analyzers.syntax_analyzer import parse   # Milestone 2

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
  cleaned = preprocess(code)
  tokens = tokenize(cleaned)

  # Validation: prints its messages, catch what it prints
  old_stdout = sys.stdout
  buffer = io.StringIO()
  sys.stdout = buffer
  try:
    validation(tokens)
  finally:
    sys.stdout = old_stdout
  validation_text = buffer.getvalue().strip()

  # (3_3) list of tokens
  token_list = []
  error_count = 0
  for lexeme, classification, line in tokens:
    token_list.append({"lexeme": lexeme, "classification": classification, "line": line})
    if classification == "Unidentified":
      error_count += 1

  # (4o4) symbol table : not needed yet
  symbol_list = []
  seen = []
  for lexeme, classification, line in tokens:
    if classification == "Variable Identifier" and lexeme not in seen:
      seen.append(lexeme)
      symbol_list.append({"identifier": lexeme, "value": "non"})

  # console text (KoK)
  if len(tokens) == 0:
    console_text = "Nothing to analyze (>n<)"
  else:
    console_text = "Lexical analysis finished: " + str(len(tokens)) + " lexemes found! (UwU)\n" + validation_text

  return jsonify({
      "tokens": token_list,
      "symbols": symbol_list,
      "errors": error_count,
      "console": console_text,
  })

def run_app():
  app.run(host=HOST, port=PORT)

if __name__ == "__main__":
  run_app()
