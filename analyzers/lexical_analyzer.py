#(OwO)==================================================================
# LEXICAL ANALYZER (Milestone 1)
# preprocess -> tokenize -> validation
#(OwO)==================================================================
import re
from typing import List, Tuple

'''
Preprocessing Code
- File Reading
- Comment Cleaning
- RegEx Cleaning
'''

def preprocess(code: str) -> List[Tuple[int, str]]:
  lines =  code.splitlines()
  cleaned_lines = []
  multiline_comment = False

  for line_number, line in enumerate(lines, start = 1):
    stripped = line.strip()

    if multiline_comment:
      if "TLDR" in stripped:
        multiline_comment = False
      continue

    if stripped.startswith("OBTW"):
        multiline_comment = True
        continue

    if "BTW" in line:
      line = re.sub(r'(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)BTW.*', '', line)

    cleaned_text = line.strip()
    if cleaned_text:
        cleaned_lines.append((line_number, cleaned_text))

  return cleaned_lines

'''
Tokenization and Classification Code
'''

KEYWORDS = [
    ("I HAS A", "Variable Declaration"),
    ("ITZ", "Variable Assignment"),
    ("R","Assignment Operator"),
    ("HAI", "Code Delimiter"),
    ("KTHXBYE","Code Delimiter"),
    ("WAZZUP", "Variable Section Start"),
    ("BUHBYE", "Variable Section End"),
    ("SUM OF","Arithmetic Operator"),
    ("DIFF OF","Arithmetic Operator"),
    ("PRODUKT OF","Arithmetic Operator"),
    ("QUOSHUNT OF","Arithmetic Operator"),
    ("MOD OF","Arithmetic Operator"),
    ("BIGGR OF","Arithmetic Operator"),
    ("SMALLR OF","Arithmetic Operator"),
    ("BOTH OF","Boolean Operator"),
    ("EITHER OF","Boolean Operator"),
    ("WON OF","Boolean Operator"),
    ("NOT","Boolean Operator"),
    ("ANY OF","Boolean Operator"),
    ("ALL OF","Boolean Operator"),
    ("BOTH SAEM","Comparison Operator"),
    ("DIFFRINT","Comparison Operator"),
    ("SMOOSH","Concatenation Operator"),
    ("MAEK","Typecast Operator"),
    ("A","Typecast Keyword"),
    ("IS NOW A","Typecast Operator"),
    ("VISIBLE","Output Keyword"),
    ("GIMMEH","Input Keyword"),
    ("O RLY?","If Keyword"),
    ("YA RLY","If Keyword"),
    ("MEBBE","ELse-If Keyword"),
    ("NO WAI","Else Keyword"),
    ("OIC","Flow Control End"),
    ("WTF?","Switch Control End"),
    ("OMG","Case Keyword"),
    ("OMGWTF","Default Case Keyword"),
    ("IM IN YR","Loop Start"),
    ("UPPIN","Loop Operation"),
    ("NERFIN","Loop Operation"),
    ("YR","Parameter Keyword"),
    ("TIL","Loop Condition"),
    ("WILE","Loop Condition"),
    ("IM OUTTA YR","Loop End"),
    ("HOW IZ I","Function Definition"),
    ("IF U SAY SO","Function End"),
    ("GTFO","Break / Return"),
    ("FOUND YR","Return Keyword"),
    ("I IZ","Function Call"),
    ("MKAY","Operation End"),
    ("AN", "Operand Separator"),
]

KEYWORDS.sort(key=lambda kw: len(kw[0]), reverse=True) #prevent matching 'OMG' already when it is infact 'OMGWTF'(all long ones are iterated first)

PATTERNS = [
    (r'"[^"]*"', "YARN Literal"),
    (r'-?[0-9]+\.[0-9]+(?![\w.])', "NUMBAR Literal"),
    (r'-?[0-9]+(?![\w.])', "NUMBR Literal"),
    (r'(WIN|FAIL)\b', "TROOF Literal"),
    (r'(NUMBR|NUMBAR|YARN|TROOF|NOOB|TYPE)\b', "TYPE Literal"),
]

KEYWORD_PATTERNS = []
for keyword, classification in KEYWORDS:
    pattern = re.escape(keyword)
    if keyword[-1].isalnum():     #treat '?' in 'O RLY?' and 'WTF?' as part of pattern
      pattern = pattern + r'\b'   #match pattern exactly how it ends
    KEYWORD_PATTERNS.append((pattern, classification))

PLUS = (r'\+', "Output Separator")
IDENTIFIER = r'[a-zA-Z][a-zA-Z0-9_]*'

def tokenize(cleaned_lines):
  tokens = []
  for line_number, text in cleaned_lines:
    pos = 0
    while pos < len(text):
      if text[pos].isspace():
        pos += 1
        continue
      test_text = text[pos:]
      for pattern, classification in PATTERNS + KEYWORD_PATTERNS + [PLUS]:     # test_text maybe a keyword
        lexeme = re.match(pattern, test_text)
        if lexeme:
          tokens.append((lexeme.group(), classification, line_number))
          pos += lexeme.end()
          break
      else:
        lexeme = re.match(IDENTIFIER, test_text)
        if lexeme:   # test_text maybe an identifier
          # get previous token
          if tokens:
            previous_token = tokens[-1][0]    #tokens[token1[lexeme, classification, line], token2, ...]
          else:
            previous_token = None

          # use the previous_token to classify what type of identifier it is
          if previous_token in ("HOW IZ I", "I IZ"):
            classification = "Function Identifier"
          elif previous_token in ("IM IN YR","IM OUTTA YR"):
            classification = "Loop Identifier"
          else:
            classification = "Variable Identifier"

          tokens.append((lexeme.group(), classification, line_number))
          pos += lexeme.end()

        else:   # test_text unidentified
          end = pos
          while end < len(text) and text[end] != " ":
            end += 1
          lexeme = text[pos:end]
          tokens.append((lexeme, "Unidentified", line_number))
          pos = end

  return tokens


'''
Token validation
'''
def validation(tokens):
  error_cnt = 0

  print("\n========================================================================\n")
  for lexeme, classification, line in tokens:
    if classification == "Unidentified":
      error_cnt += 1

      # unclosed quotation
      if lexeme.startswith('"') and not lexeme.endswith('"'):
        print(f"[Line {line}] Syntax Error: Unclosed string literal '{lexeme}'")

      # more than one decimal point
      elif "." in lexeme and lexeme.count(".") > 1:
        print(f"[Line {line}] Syntax Error: Invalid decimal declaration '{lexeme}'")

      # invalid decimal point placement
      elif lexeme.endswith(".") or (lexeme.startswith(".") and len(lexeme) == 2 and lexeme[1].isdigit()):
        print(f"[Line {line}] Syntax Error: Invalid decimal declaration '{lexeme}'")

      # literal starts with num (ex. 3num)
      elif any(char.isdigit() for char in lexeme) and any(char.isalpha() for char in lexeme):
        print(f"[Line {line}] Syntax Error: Invalid literal or identifier '{lexeme}'")

      # special char w/o quotations
      elif not lexeme.isalnum() and not lexeme.startswith('"'):
        print(f"[Line {line}] Syntax Error: Invalid symbol or unexpected token '{lexeme}'")

      # default case
      else:
        print(f"[Line {line}] Syntax Error: Unidentified token '{lexeme}'")

  print(f"\nTotal errors found: {error_cnt}")
