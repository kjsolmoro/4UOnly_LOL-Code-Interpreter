# PAANO GUMAGANA YUNG PARSER (the whole idea)
# ---------------------------------------------------------------
# 1. FROM SA OUTPUT NI LEXER (simulan natin dito) 
# ---------------------------------------------------------------
# Yung lexical analyzer natin dba ginagawang TOKENS yung LOLCode
# Bawat token ay (lexeme, classification, line):
#
#     HAI                ->  ("HAI", "Code Delimiter", 1)
#     GIMMEH x           ->  ("GIMMEH", "Input Keyword", 2), ("x", "Variable Identifier", 2)
#     KTHXBYE            ->  ("KTHXBYE", "Code Delimiter", 3)
#
#   token[0] = lexeme          (yung mismong word)
#   token[1] = classification  (anong klase)
#   token[2] = line            (anong line, para sa error message)
#
# Sa app.py: kpag may LEXICAL error, HINDI na mag run yung parser.
# Kung wala, ipapasa yung tokens kay parse().
#
# ---------------------------------------------------------------
# 2. parse(tokens)  -  syntax_analyzer.py  (ung entrance )
# ---------------------------------------------------------------
#   a) add_linebreaks(tokens)
#        Diba sa preprocess tinanggal ng lexer ung newlines, kailangan natin sila ibalik
#        kasi yun yung mag s serve ling saan mag e end ung mga grammer 
#        basta ang nangyari lang dun ay:  
#        from:  HAI, GIMMEH, x, KTHXBYE
#        to:    HAI, \n, GIMMEH, x, \n, KTHXBYE, \n
#
#   b) then gagawa na tayo ng parser, dictionary lang sya.
#        ang idea lang nung "parser" ay para ma track lng natin kung nasaan part na tayo
#        at kung ano na yung currently na i p parse.
#        kaya sya ganto:
#          parser = {"tokens": [...], "position": 0}
#               **diba napagusapan ntin sa meeting is list tapos ipapasa pasa na lang sa mga 
#                   functions/grammar yung mga specific parts na needed sa grammar.
#                   trinay ko ganon kaso, ang hirap ksi chop chopin pa list tapos di mo din alam
#                   kung hanggang saan chop chopin mo. kayo ganto na lng naisip k na approach which is
#                   ipasa na lng natin ng buo pero track natin kung saan part na tayo
#                  
#        "position" = isipin nyo n lng na para syang daliri na nakaturo sa kung anong part na yung i p parse
#
#   c) tatawagin si parse_program(parser)  -> dito na magsimula yung checking ng grammar. ibabato n natin si parser 
#                                              kay parse_program() which is basically ung unang grammar natin (check proj req 2)
#
#   d) sa result naman ay:
#        walang error  -> return []                          (no syntax errors)
#        may error     -> return ["Line X: ..."]         (yung error message)
#                           *[] list lang yan na paglalagyan ng error na makikita, na ibabato ntin pabalik sa app.py para i display
#
# ---------------------------------------------------------------
# 3. Eto na exciting na part HAHAHA eto na ung recursive kineme. 1 GRAMMAR RULE = 1 FUNCTION
# ---------------------------------------------------------------
# Ang idea is bawat rule sa Req 2 ay may sariling parse_ function. Binabasa ng function
# yung rule niya from LEFT to RIGHT:
#
#     <input> ::= GIMMEH varident       //eto ung grammar rule diba
#
#     def parse_input(parser):              
#       expect(parser, "GIMMEH")                                         # keyword
#       expect_class(parser, "Variable Identifier", "a variable name")   # klase ng token
#
#     **omg what's this what's that?!?! hahaha ems simple lng yan, eto sinasabi ko na pattern pattern lang haha
#          [tignan nyo na lng sya pababa] 
#     <input>       def parse_input(parser)
#     ::=           :
#     GIMMEH        expect(parser, GIMMEH)
#     varident      expect_class(parser, "Variable Identifier", "a variable name")
#
#   gets ba? hahaha basically ganyan lng idea (check nyo n lng yung mga gawa ko sa statements.py -> functions.py -> program.py)
#   some patterns na makita nyo:
#       keyword (AN, OIC)    ->  expect(parser, "AN")
#       klase ng token       ->  expect_class(parser, "Variable Identifier", "...")
#       ibang rule <...>     ->  tawagin yung function niya: parse_operand(parser)
#       ε                    ->  makikita nyo gumamit ako ng if: kung andun, i-parse; kung wala, walng gagawin
#       yung mga tinatawag sarili naman ay(recursive) ->  makita nyo guys gumamit ako while loop (WAG NYO ILAGAY sariling function sa loob nya)
#                                                                                             **learned it the hard way, just trust me bro n lng haha  
# ---------------------------------------------------------------
# 4. basic ideas lang nung helper functions (helpers.py) **itrack nyo isa isa para mas magets
# ---------------------------------------------------------------
#   peek(parser)          -> tingnan ung current token na pinaparse (remember ung sa "parser" ntin)      
#   peek_next(parser)     -> tingnan ung kasunod na token (silip lang)
#   advance(parser)       -> move sa next token na ipaparse
#   expect(parser, w)     -> check kung ung current na pinaparse natin ay yung ineexpect natin na lexeme(keyword); 
#                             kung oo: advance, kung hindi: error
#   expect_class(...)     -> same sa expect pero yung classidication naman 
#   parse_linebreak(...)  -> remember binalik natin yung mga "\n" 
#                               **malaki kasi role nila sa grammar, kasi ung ibang grammar rules one-line lang hindi tulad nung
#                                   ibang rules na may keyword na magsisignify as end. also buffer din yan para yung expect() 
#                                   function natin (which is nagc check sa ineexpect na kasunod na token diba) ay may \n pa rin
#                                   na mapagc comparean at hindi mag expect sa WALA (pain, pighati, lumbay, aguy, huhu)
#   error(parser, msg)    -> partner to ni expect() pag hindi tama yung token na ineexpect natin, stop function na tapos r report 
#                           lang nya yung error "Line X: <msg>, but found <token>" tapos ibabato na nya pabalik kay 
#                           syntax_analyzer.py (notice nyo ung try-catch dun) 
#
# ---------------------------------------------------------------
# 5. how to visualize yung workflow
# ---------------------------------------------------------------
#   Code:
#       HAI
#          GIMMEH x
#       KTHXBYE
#
#   Lexer:
#       HAI, GIMMEH, x, KTHXBYE
#
#   parse():
#       parser = HAI, \n, GIMMEH, x, \n, KTHXBYE            
#                (*)                                        note: (*) is parser currently pointing 
#       parse_fn1(parser)
#
#   Example grammar rules:
#       <fn1> ::= HAI \n <fn2> <KTHXBYE>
#       <fn2> ::= GIMMEH <fn3> \n
#       <fn3> ::= x
#
#   [di ko na inisa isa bawat steps, imagine nyo na lng nagsimula na ung code hanggang sa nakating na tayo sa point na nasa baba]
#
#           def parse_fn1(parser):                               def parse_fn2(parser):                         def parse_fn3:
#               HAI         //done                                   GIMMEH      //done                             x  //done
#               \n          //done                                   parse_fn3(parser)  //done      
#               parse_fn2(parser)   // waiting parse_fn2             \n          // CURRENTLY DOING
#               KTHXBYE     //not done
#
#           HAI, \n, GIMMEH, x, \n, KTHXBYE              
#                               (*)   
#         ===================================================================================================================
#
#           def parse_fn1(parser):                               def parse_fn2(parser):                         def parse_fn3:
#               HAI         //done                                   GIMMEH      //done                             x  //done
#               \n          //done                                   parse_fn3(parser)  //done      
#               parse_fn2(parser)  //done                            \n          //done
#               KTHXBYE     //currently doing
#
#           HAI, \n, GIMMEH, x, \n, KTHXBYE              
#                                     (*)      
#         
#   basically ang idea na dapat makita nyo lang is
#       - diba binigyan tayo ng list ng tokens, pero di natin alam kung tama ba yung SYNTAX NG BUONG CODE
#       - di natin maidentify yung SYNTAX NG BUONG CODE kasi binubuo to ng ibat ibang MAS MALILIIT na rules
#         (sa example: buong program = fn1, sa loob nya si fn2, sa loob ni fn2 si fn3)
#       - kaya bawat rule = 1 function, at sarili lang nyang rule yung chine-check nya
#       - pag nakarating sya sa part na ibang rule (ex. si fn1 nakarating sa <fn2>),
#         tatawagin nya yung function nun, tapos MAGHIHINTAY lang sya hanggang matapos
#       - pagbalik, tuloy lang sya kung saan sya huminto (ex. si fn1 tuloy sa KTHXBYE)
#       - iisa lang yung (*) / position, kaya kahit sino gumalaw, alam ng lahat kung nasaan na tayo
#           ** yun din yung reason kung bakit [try looking at machine's perspective] na kahit wala tayo idea kung hanggang  
#              saan matatapos (di alam yung full picture ng scope) ay nagagawa pa din natin tumama sa kung ano yung ineexpext
#              natin na next makita given only nasa simulang part ka palang
#       - pag natapos lahat ng function na walang mali -> follows the grammar -> tama yung syntax ng buong code
#         pag may isang mali naman kahit nasaan pa siya -> titigil lahat -> error    


from analyzers.lexical_analyzer import preprocess, tokenize
from analyzers.syntax.helpers import add_linebreaks, parse_linebreak, peek, advance, error, LOLSyntaxError
from analyzers.syntax import expressions, statements, functions, program, flow_control
from analyzers.syntax_analyzer import parse

# ========================================== TEST_PARSER ==========================================================

# Para ma-test niyo yung functions niyo isa isa. Basically eto lang din yung nasa syntax_analyzer natin w/o 
# the GUI (sa terminal na lng para less hassle na paulit ulit i run yung app.py atsaka may options for specific func lang na gusto i run at test)
#
# HOW TO RUN (lipat nyp na lng to si test_parser.py sa repo root, kung nasaan si app.py, currently kasi nakalagay sya sa test_lol):
#       then type "py test_parser.py" sa terminal 
#
# HOW TO READ THE OUTPUT:
#     OK     | <code>                   -> tinanggap ng function mo yung code
#     ERROR  | <code> -> Line X: ...    -> ni-reject niya, with the reason
#     "... is not written yet"          -> naka-not_written() pa yung function na yun (btw tanggalin nyo yun pag nagawa nyo na grammar)
#
# NOTEE! : WAG I-COMMIT TONG FILE NA TO, i gitignore nyo muna 

def make_parser(code):
  # create lang ng parser na nadiscuss sa taas
  return {"tokens": add_linebreaks(tokenize(preprocess(code))), "position": 0}

def one_line(code):
  # pang-print lang: "WAZZUP\nI HAS A x" -> "WAZZUP / I HAS A x"
  return code.replace("\n", " / ")

def check_program(code):
  # kung gusto mo magtest na parang buong syntax analyzer na 
  # note: yung may HAI ... KTHXBYE
  errors = parse(tokenize(preprocess(code)))
  if errors:
    print("ERROR  |", one_line(code), "->", errors[0])
  else:
    print("OK     |", one_line(code))

def check(parse_function, code):
  # kung gusto mo magtest ng certain function lang sa code
  # note: gamitin mo lng to sa mga functions na may sariling linebreak na o dikaya ung mga pwedeng "ε"
  parser = make_parser(code)
  try:
    parse_function(parser)
    print("OK     |", one_line(code))
  except LOLSyntaxError as e:
    print("ERROR  |", one_line(code), "->", e)
 
def check_line(parse_function, code):
  # same sa check() pero pagkatpos ng function mo, dapat tapos na yung line
  # note: maganda to panghuli sa sobrang tokens ex. "GIMMEH x y" -> ERROR sa 'y'
  def function_then_end_of_line(parser):
    parse_function(parser)      # eto function mo diba tapos kunyari tapos na and nagmove na yung tinuturo ni parser
    parse_linebreak(parser)     # sa part na to sasaluhin na nya yung \n. pag may ibang token na nakita or sumobra, huli sya kasi dapat \n na last
  check(function_then_end_of_line, code) 
 
def show_tokens(code):
  # priint tokens lang pang debug
  for lexeme, classification, line in make_parser(code)["tokens"]:
    if lexeme == "\n":
        lexeme = "\\n"
    print(f"  line {line}: {lexeme:<15} {classification}")

def my_examples():
  print("\n---- show_tokens----")
  show_tokens("HAI\nGIMMEH x\nKTHXBYE")

  print("\n---- check_line: isang statement ----")
  check_line(statements.parse_input, "GIMMEH x")                 # OK
  check_line(statements.parse_input, "GIMMEH")                   # ERROR kulang variable
  check_line(statements.parse_input, "GIMMEH x y")               # ERROR sobra
  check_line(statements.parse_input, "GIMMEH 5")                 # ERROR mali classication, variable identifier dpt
 
  print("\n---- check_line: multi-line ----")
  check_line(functions.parse_func_def, "HOW IZ I greet\nGIMMEH x\nIF U SAY SO")   # OK
  check_line(functions.parse_func_def, "HOW IZ I greet\nGIMMEH x")                # ERROR walang closing (IF U SAY SO)
  check_line(functions.parse_func_def, "HOW IZ I greet\nGIMMEH\nIF U SAY SO")     # ERROR sa loob 
 
  print("\n---- check: sariling linebreak / empty ----")
  check(program.parse_var_section, "WAZZUP\nI HAS A x\nBUHBYE")   # OK
  check(program.parse_var_section, "")                            # OK  ε sa grammar optional lang si WAZZUP
 
  print("\n---- check_program ----")
  check_program("HAI\nGIMMEH x\nKTHXBYE")                         # OK
  check_program("HAI\nGIMMEH x")                                  # ERROR walang KTHXBYE
 
def my_tests():
  print("\n---- test ----")
  # dito nyo ilagay test nyo ex: 
  # check_line(<file>.<parse_function>, "...")
  # btw kung alin sa check/check_line/check_program ba ang gagamitin ay depende sa grammar nyo  

my_examples()       #uncomment nyo na lang
# my_tests()    