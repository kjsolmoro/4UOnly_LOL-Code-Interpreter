# PAANO GUMAGANA YUNG SEMANTIC ANALYZER (the whole idea)
#
# ---------------------------------------------------------------
# lagay ako analogy para mas madali ma visualize hahah
# ---------------------------------------------------------------
#   premise: umalis si nanay nagtrabaho, tapos nag iwan sya ng LISTAHAN NG UTOS sa ref.
#   ikaw yung gagawa ng mga nakalista. yung listahan na yun = yung .lol file
#
#     1) LEXER (Milestone 1) -> binabasa mo lng yung bawat SALITA
#           "totoong salita ba to?"
#           "Bmili ng itlg"                  -> ha? nudaw? mali yung salita        (lexical error)
#
#     2) PARSER (Milestone 2) -> chinecheck mo kung BUO yung bawat utos
#           "buo ba yung sentence? may kulang ba?"
#           "Bumili ng ___ sa"               -> ano bibilhin? saan? kulang          (syntax error)
#
#     3) SEMANTIC (Milestone 3) -> dito GINAGAWA mo na talaga isa isa, from taas pababa
#           dito mo lng malalaman kung may utos pala na di kaya gawin kasi mali:
#           "Iabot kay Tita yung sukli"          pero wala ka naman binili, walang sukli   -> ERROR (walang dinclare na sukli)
#           "Hatiin yung 10 pandesal sa 0 tao"   mathematically wrong                      -> ERROR (di kaya ievaluate)
#           "Bumili ng 'marami' na itlog"        ilan nga?? hindi number si "marami"       -> ERROR (kumbaga mali sa data type)
#
#   **si semantic analyzer na yung GUMAGAWA ng mga utos (interpreter)
#     sya na yung naglalabas ng output sa console tsaka yung laman ng symbol table
#
#     listahan ni nanay      =  LOLCode program
#     isang utos             =  isang statement
#     ginagawa mo isa isa    =  semantic analyzer (run)
#
# ---------------------------------------------------------------
# 1. FROM SA OUTPUT NI PARSER (simulan natin dito)
# ---------------------------------------------------------------
# nung Milestone 2 chinecheck lng ni parser kung TAMA yung grammar. ngayon habang nagc check sya,
# BINUBUO na rin nya yung program as a tree (AST = Abstract Syntax Tree).
# bawat statement = isang dictionary (node) na may "type" para alam natin kung ano sya:
#
#     HAI
#     WAZZUP
#       I HAS A x ITZ 5
#     BUHBYE
#     VISIBLE SUM OF x AN 2
#     KTHXBYE
#
#   nagiging:
#
#     {"type": "program",
#      "functions":    [],                                         <- mga HOW IZ I
#      "declarations": [{"type": "declare", "var": "x",            <- laman ng WAZZUP
#                        "init": ("5", "NUMBR Literal", 3), "line": 3}],
#      "body":         [{"type": "print", "line": 5,               <- mga statement
#                        "args": [{"type": "arithmetic",
#                                  "op":    ("SUM OF", "Arithmetic Operator", 5),
#                                  "left":  ("x", "Variable Identifier", 5),
#                                  "right": ("2", "NUMBR Literal", 5)}]}]}
#
#   **pansinin nyo: yung pinakadulo ng tree ay TOKEN pa rin (lexeme, classification, line)
#     yung mga may "type" naman ay nodes na may laman pang ibang nodes or tokens
#   **every statement may "line" na, para pag may semantic error alam natin kung saang line
#
#   kung gusto pala makita tree = show_ast(code) sa baba (eto ung sa docs: PARSE TREE VISUALIZATION)
#
# ---------------------------------------------------------------
# 2. run(ast)  -  semantic_analyzer.py  (ung entrance)
# ---------------------------------------------------------------
#   a) gagawa ng 2 dictionary: scope tsaka runtime (explained sa #5)
#        scope   = {"IT": None}            <- si IT laging andyan, NOOB muna 
#        runtime = {"functions": {}, "output": [], "inputs": [...], "next_input": 0, "line": 0}
#
#   b) i register lahat ng HOW IZ I     -> para matawag sila kahit nasa baba pa (after KTHXBYE)
#   c) i run yung WAZZUP declarations  -> exec_declare() bawat isa
#   d) i run yung body                 -> execute_code_block() -> execute_statement() isa isa
#
#   e) sa result naman ay:
#        {"output":     "laman ng lahat ng VISIBLE o mga i p print sa console",
#         "symbols":    [{"identifier": "x", "value": "5", "type": "NUMBR"}, ...],   <- symbol table
#         "errors":     [] or ["line n: semntic error ..."],
#         "need_input": None or "pangalan ng variable na paglalagyan ng input galing user"}    <- para kay GIMMEH (dito ka Z kasi connected to sa GUI)
#
#   **parang syntax analyzer lng din: pag may error kahit saan, titigil lahat tapos ibabalik yung error
#
# ---------------------------------------------------------------
# 3. eto yung pattern. 1 NODE TYPE = 1 FUNCTION
# ---------------------------------------------------------------
# same idea sa parser (1 grammar rule = 1 function). dito naman bawat "type" ng node may sariling function:
#
#     {"type": "print", ...}         ->  exec_print(node, scope, runtime)          (statements.py)
#     {"type": "assign", ...}        ->  exec_assign(node, scope, runtime)         (statements.py)
#     {"type": "if_then", ...}       ->  execute_if_then(node, scope, runtime)     (flow_control.py)
#     {"type": "arithmetic", ...}    ->  eval_arithmetic(node, scope, runtime)     (expressions.py)
#
#   2 klase lng ng nodes:
#       STATEMENT  -> may GINAGAWA (nagpi print, nagbabago ng variable)   -> si execute_statement() nag aassign  
#       EXPRESSION -> may VALUE na binabalik (SUM OF x AN 2 -> 7)          -> si evaluate_expression() nag aassign
#
#   gets ba? parehas lng sila ng parse_statement() ntin, malaking if/elif na tinitingnan yung "type"
#   tapos ipapasa sa tamang function. pag gagawa kayo ng bago, ganto lng:
#       1. tingnan nyo sa show_ast() kung anong "type" tsaka anong laman ng node nyo
#       2. dagdagan ng elif sa execute_statement() / evaluate_expression()  (andun na yung iba, check nyo mupna)
#       3. isulat ung function. sa loob, evaluate_expression() lng ulit sa mga parts (left, right, args)
#
# ---------------------------------------------------------------
# 4. VALUES: plain Python values lng
# ---------------------------------------------------------------
#   dati (ung pinush ni rein) every value may kasamang type:  (17, "NUMBR")
#   ngayon value na lng, kasi yung Python type na mismo yung nagsasabi:
#
#     LOLCode    Python      example
#     NOOB       None        None
#     TROOF      bool        True / False
#     NUMBR      int         17
#     NUMBAR     float       3.14
#     YARN       str         "hello"
#
#   type_of(17) -> "NUMBR"   type_of("hi") -> "YARN"   (typecast.py)
#
#   lahat ng casting nasa typecast.py lng:
#       to_troof()       -> "" / 0 / NOOB = FAIL, others WIN
#       to_num()         -> pang math (implicit). "12" -> 12, "abc" -> error, NOOB -> error
#       to_yarn()        -> pang VISIBLE/SMOOSH (implicit). 3.14 -> "3.14" 
#       cast_explicit()  -> pang MAEK tsaka IS NOW A. same rules pero NOOB -> 0 / "" / FAIL imbis na error
#
#   (eto ung sa docs: RUNTIME TYPE COERCION)
#        
# ---------------------------------------------------------------
# 5. scope vs runtime (balik sa analogy)
# ---------------------------------------------------------------
#   scope   = yung BULSA mo. dito yung mga hawak mo habang ginagawa yung utos
#               ex. pera, sukli, resibo          -> variables (x, y, IT)
#             **si IT = yung huling inabot sayo / huling sagot na hawak mo. 
#                       (checck nyo sa #2 balik kayo, makita nyo nakalagay na sya agad diba? bakit? isipin nyo yun yung hangin ng bulsa nyo, represents "wala" haha)
#
#   runtime = yung BAHAY. shared ng lahat ng tao sa bahay, hindi kanino lng:
#               - pinto ng ref           -> output     lahat ng VISIBLE dun dinidikit, kahit sino nagsulat          eto yung mga prinint sa console ntin
#               - text ni nanay          -> inputs     pag GIMMEH, hihintayin mo reply ni nanay (user),
#                                                      binabasa isa isa in order 
#               - listahan sa pader      -> functions  lahat ng HOW IZ I (ex. "si bunso marunong magsaing")
#               - checklist ng utos      -> line       kung saang utos ka na, para alam mo kung saan nagkamali
#
#   pag may function call (I IZ ...), parang inutusan mo si BUNSO na gawin yung isang utos:
#       - may SARILING BULSA si bunso (bagong scope)
#       - iaabot mo lng yung kailangan nya, nakasulat sa papel (args)
#           -> pero kopya lng yun, kaya kahit sulatan nya yung papel di magbabago yung nasa bulsa mo
#       - syempre HINDI sya pwede dumukot sa bulsa mo
#       - pero SAME BAHAY pa rin:
#           -> yung sinulat nya (VISIBLE) sa parehong ref din didikit
#           -> pag nag GIMMEH sya, yung SUSUNOD na text ni nanay yung mababasa nya (hindi yung nabasa mo na)
#       - pagbalik nya, iaabot nya sayo yung result (FOUND YR/return call) -> yun na yung bagong IT mo
#
#     bulsa mo              =  scope ni main
#     bulsa ni bunso        =  scope ng function (bago every call)
#     bahay                 =  runtime (iisa lng, shared)
#
#   **btw eto pala binago ko rein: dati kasi diba interp lang nakalagay. kumbaga iisa lng yung bulsa ng LAHAT. kaya pag inutusan mo si bunso,
#     ilalabas mo pa muna lahat ng laman ng bulsa mo, ipapahiram, tapos ibabalik pagkatapos.
#     ngayon may sariling bulsa na si bunso, parehong bahay pa rin. walang kailangan ilabas at ibalik (eto ung sa docs: VARIABLE SCOPING RESOLUTION)
#
# ---------------------------------------------------------------
# 6. GTFO, FOUND YR, GIMMEH -> exceptions gamit (errors.py)
# ---------------------------------------------------------------
#   LOLSemanticError -> totoong error. titigil buong program, lalabas sa console
#   BreakSignal      -> GTFO.       sasaluhin ng pinakamalapit na loop / switch / function
#   ReturnSignal     -> FOUND YR.   sasaluhin ng function call, dala nya yung value
#   NeedsInputSignal -> GIMMEH pero wala pang tinype yung user 
#
#   mga exceptions para parang di na pagpasapsahan pa, kusa na AAKYAT pataas hanggang may sumalo (try/except).
#   **btw same idea lng ng LOLSyntaxError sa parser (yung try-catch sa syntax_analyzer.py)
#
#   **IMPORTANTE (Member 3): yung loop tsaka switch, BreakSignal LNG yung sasaluhin. wag ReturnSignal
#     kasi pag FOUND YR sa loob ng loop sa loob ng function, dapat umakyat sya hanggang function call
#
# ---------------------------------------------------------------
# 7. how to visualize yung workflow
# ---------------------------------------------------------------
#   Code:
#       HAI
#       WAZZUP
#         I HAS A x ITZ 5
#       BUHBYE
#       VISIBLE SUM OF x AN 2
#       KTHXBYE
#
#   run(ast):
#       scope = {"IT": None}         runtime["output"] = []                          
#
#   WAZZUP -> exec_declare(declare node)
#       evaluate_expression(("5", "NUMBR Literal", 3))    -> 5
#       scope = {"IT": None, "x": 5}
#
#   body -> execute_statement(print node) -> exec_print()
#       evaluate_expression(arithmetic node)       // WAITING
#           eval_arithmetic()
#               evaluate_expression(("x", "Variable Identifier", 5))  -> scope["x"] -> 5            
#               evaluate_expression(("2", "NUMBR Literal", 5))        -> 2
#               to_num(5) = 5, to_num(2) = 2, SUM OF -> 5 + 2 = 7     (parehong int -> NUMBR)
#       evaluate_expression(arithmetic node)       // done -> 7
#       to_yarn(7) -> "7"
#       runtime["output"] = ["7\n"]
#
#   result:
#       output  -> "7"
#       symbols -> IT = NOOB (NOOB), x = 5 (NUMBR)
#
#   basically ang idea na dapat makita nyo lng is
#       - naadjust yung syntax analyzer natin. ginawa na ni parser yung tree, kaya hindi na natin binabasa yung tokens isa isa
#       - statement = may ginagawa, expression = may binabalik na value
#       - pwedeng may expression sa loob ng expression (SUM OF x AN SUM OF y AN 2) kaya recursive
#         si evaluate_expression(), tatawagin nya sarili nya hanggang sa makarating sa token ("5", "NUMBR Literal", 3) na lng
#         **eto ung chinat ko sa gc na hanggang makarating sa dulo
#       - parang parser din: maghihintay yung nasa labas hanggang matapos yung nasa loob
#       - lahat ng variables nasa scope, lahat ng shared nasa runtime
#
# ---------------------------------------------------------------
# eto pala mga changes sa gawa mo rein sa PR #8 narestructure sa PR #9
# ---------------------------------------------------------------   
#   KEPT:
#     - yung AST. lahat ng parse_ function nag rereturn na ng node {"type": "...", "args": [...]}
#     - yung file split ng semantic/ (statements, expressions, flow_control, functions) napalitan lang si helper -> typecast
#     - lahat ng function names at pagkaka structure
#     - expressions.py: same maliban sa changes na nasa baba (a)
#     - helper.py -> typecast.py: same lang din maliban sa (a) 
#     - numbar_to_yarn(): same idea ng format_value() 
#     - yung "already declared" check ng declare_symbol() -> nasa exec_declare() na
#     - yung "not declared" check ng get_symbol() -> nasa evaluate_expression() tsaka check_declared()
#     - si IT na laging una sa symbol table (snapshot_symbols mo) -> ganun pa rin
#     - yung signals (BreakSignal, ReturnSignal, NeedsInputSignal) -> nilabas lang sa errors.py 
#     - eval_comparison logic (number vs number, magkaibang type = FAIL) -> nilipat lng sa values_equal()
#       para magamit din ni switch (OMG) since may expression na c computin din dun

#     - yung mga COMMENTS/DOCSTRING di pa yun updated, nakabase pa sya sa PR #8, wag masyado pagbasehan haha 
#
#   CHANGES:
#     a) (value, type) pairs -> value lng
#          dati:   return (int(lexeme), "NUMBR")          ngayon:  return int(lexeme)
#          dati:   n1, t1 = to_num(left_val, left_type)   ngayon:  n1 = to_num(left_val)
#        aditional function type_of() yung Python type na mismo yung ginamit na type na pinagcomparean
#     b) interp -> scope + runtime  (naexplain sa taas #5)
#     c) declare_symbol, get_symbol, update_symbol, set_it, get_it -> scope["x"] na lng direkta
#        snapshot_symbols -> symbol_table() sa semantic_analyzer.py (may "type" na rin)
#     d) helpers.py -> typecast.py (casting lng) + errors.py (LOLSemanticError tsaka signals)
#     e) parser: lahat ng statement tsaka declaration may "line" na, MAEK dapat type sa dulo
#
#
# ---------------------------------------------------------------
# Z, NICA
# --------------------------------------------------------------- 
#
#   a) git checkout main -> git pull -> git checkout -b <branch nyo>
#   b) i run tong file: python test_lol/test_semantic.py   -> tingnan nyo yung "sample itsura" sa output
#      andun yung itsura ng mga node nyo (show_ast), para alam anong keys ung kukunin
#   c) yung pattern: tingnan nyo si exec_print() tsaka exec_assign() sa statements.py, ganun lng din
#        - kunin yung laman ng node:     node["var"], node["ya_rly"], node["cond"],
#        - i evaluate yung expressions:  evaluate_expression(expr, scope, runtime)
#        - i run yung blocks:            statements.execute_code_block(block, scope, runtime)
#        - pag may mali:                 raise LOLSemanticError("...")
#
#   TOOLS na pwede nyo gamitin (andyan na, tawagin nyo na lng):
#     evaluate_expression(expr, scope, runtime)        -> value ng expression            (expressions.py)
#     values_equal(a, b)                               -> pang compare, gamit ni OMG       (expressions.py)
#     statements.execute_code_block(block, scope, runtime)  -> i run yung list ng statements
#     statements.check_declared(name, scope)           -> error kung wala yung variable
#     to_troof(value)  to_num(value)  cast_explicit(value, "NUMBR")                       (typecast.py)
#     raise BreakSignal() / NeedsInputSignal(var)      -> galing errors.py
#
#   Z: GIMMEH + app.py + browser
#     node:   {"type": "input", "var": "x", "line": 5}
#     1. exec_input() sa statements.py
#          - check_declared(node["var"], scope)
#          - kung ubos na inputs: raise NeedsInputSignal(node["var"])
#          - else kunin runtime["inputs"][runtime["next_input"]], tapos +1 sa runtime["next_input"]
#            (para ung nexxt GIMMEH, next input na makukuha), ta[ps wag kalimutan ilagay sa scope as YARN (str)
#     2. app.py (sira pa app.py. di pa kasi tinatawag si semantic analyzer dun atsaka nabago din nirereturn ni syntax_anlyzer. (kaya sa run_lol muna nagr run))
#     3. kailangan din kasi yung console dapat nag aaccept ng input kay user, tapos i resend yung code + lahat ng inputs
#        **btw technically di talaga natin live na binibigay yung input from user tapos nag r run at the same time,
#           ang nangyayari lang ay talaga ay nir rerun ng rerun lang hanggang makumpleto ung input na kailangan kaya dapat may inputs =[] sa app
#     4. test:  python run_lol.py test_lol/02_gimmeh.lol
#           **pag gumagana na jan, pwede na ayusin yung sa app.py at console  
#
#   NICA: IS NOW A + if / switch / loops
#     nodes nyo (tingnan n lng examples output):
#       {"type": "recast", "var": "x", "target_type": "YARN"}
#       {"type": "if_then", "ya_rly": [...], "mebbes": [{"condition": ..., "body": [...]}], "no_wai": [...] or None}
#       {"type": "switch", "cases": [{"value": <literal>, "body": [...]}, ...], "default": [...] or None}
#       {"type": "loop", "label": "lp", "op": "UPPIN"/"NERFIN", "var": "i",
#                        "cond": {"kind": "TIL"/"WILE", "expr": ...} or None, "body": [...]}
#     1. exec_recast():      cast_explicit(scope[var], node["target_type"]) tapos ibalik sa scope
#     2. execute_if_then():  to_troof(scope["IT"]) -> ya_rly; else mebbes isa isa; else no_wai (kung meron)
#     3. execute_switch():   hanapin yung unang OMG na values_equal(IT, value). from dun i run LAHAT pababa
#                             + default, hanggang GTFO -> try/except BreakSignal
#     4. execute_loop():     while True: check cond (TIL = stop pag WIN, WILE = stop pag FAIL),
#                            run body (try/except BreakSignal -> break), UPPIN +1 / NERFIN -1 sa var
#        **BreakSignal LNG yung sasaluhin, wag ReturnSignal (#6 sa taas)
#        **i set nyo runtime["line"] = node["line"] bago i check yung cond para tama yung line sa error
#     5. test: 07, 08, 09 (kaso may mga GIMMEH kasi yun, need muna matapos yun) alternatively pwede naman
#        gawa kayo ng sariling maliit na lol program sa tests() using check_program() tapos walang gimmeh.
#        pero pag tapos naman na gimmeh (pero sira pa GUI) pwede i test 07, 08, 09 using run_lol.py
#

import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  

from analyzers.lexical_analyzer import preprocess, tokenize
from analyzers.syntax_analyzer import parse
from analyzers.semantic_analyzer import run

# ========================================== TEST_SEMANTIC ==========================================================

# para ma test nyo yung part nyo isa isa sa terminal incase di pa working GUI
#
# HOW TO RUN (sa repo root, kung nasaan si app.py):
#       python test_lol/test_semantic.py
#
# HOW TO READ THE OUTPUT:
#     show_ast                              -> yung tree na binigay ni parser (para alam laman ng node nyo)
#     OK    | <expr> -> <value> (<TYPE>)    -> yung value ng expression tsaka type nya
#     ERROR | ...                           -> error
#     "gawin muna ..."                      -> hindi pa nagagawa
#
# para sa buong program na may GIMMEH na pero di pa ayos GUI, gamitin nyo na lng yung run_lol.py sa root

def one_line(code):
  # pang print lng: "HAI\nVISIBLE x" -> "HAI / VISIBLE x"
  return code.replace("\n", " / ")

def short(node):
  # pinaikli lng yung token para mas madali basahin: ("5", "NUMBR Literal", 3) -> 5
  if type(node) == tuple:
    return node[0]
  if type(node) == list:
    return [short(x) for x in node]
  if type(node) == dict:
    return {key: short(value) for key, value in node.items()}
  return node

def show_ast(code):
  # pang debug: tingnan yung tree. naka short() kaya lexeme lng yung tokens
  result = parse(tokenize(preprocess(code)))
  if result["errors"]:
    print("SYNTAX ERROR |", result["errors"][0])
    return
  ast = result["ast"]
  for name in ["functions", "declarations", "body"]:
    print(f"  {name}:")
    for node in ast[name]:
      print("   ", short(node))

def check_expr(expr):
  # i run yung isang expression tapos tingnan kung ano value nya sa IT
  # note: walang variables dito, literals lng (gamitin nyo si check_program kung may variables)
  answer = run_program_quietly("HAI\n" + expr + "\nKTHXBYE")
  if answer is None:
    return
  if answer["errors"]:
    print("ERROR |", expr, "->", answer["errors"][0])
  else:
    it = answer["symbols"][0]            # laging una si IT sa symbol table
    print(f"OK    | {expr} -> {it['value']} ({it['type']})")

def check_program(code, inputs=None):
  # parang buong interpreter na: output, error, tapos symbol table
  print("\nPROGRAM |", one_line(code))
  answer = run_program_quietly(code, inputs)
  if answer is None:
    return
  print("  output :", repr(answer["output"]))
  if answer["errors"]:
    print("  error  :", answer["errors"][0])
  if answer["need_input"]:
    print("  waiting for GIMMEH", answer["need_input"])
  for row in answer["symbols"]:
    print(f"  {row['identifier']:<10} {row['value']:<15} {row['type']}")

def run_program_quietly(code, inputs=None):
  # lexer -> parser -> semantic. pag may syntax error, ipi print lng tapos None
  result = parse(tokenize(preprocess(code)))
  if result["errors"]:
    print("SYNTAX ERROR |", one_line(code), "->", result["errors"][0])
    return None
  return run(result["ast"], inputs or [])

def my_examples():
  print("\n---- show_ast ----")
  show_ast("HAI\nWAZZUP\n  I HAS A x ITZ 5\nBUHBYE\nVISIBLE SUM OF x AN 2\nKTHXBYE")

  print("\n---- check_expr: math + typecasting ----")
  check_expr("SUM OF 2 AN 3")                 # 5 (NUMBR)
  check_expr("SUM OF \"2\" AN 3.0")           # 5.00 (NUMBAR)  YARN -> number, may NUMBAR kaya NUMBAR
  check_expr("QUOSHUNT OF 7 AN 2")            # 3 (NUMBR)      int / int -> int, cut lng
  check_expr("MAEK 3.14159 YARN")             # 3.14 (YARN)
  check_expr("BOTH SAEM 1 AN 1.0")            # WIN (TROOF)    parehong number
  check_expr("SUM OF \"abc\" AN 1")           # ERROR          hindi number si "abc"
  check_expr("QUOSHUNT OF 1 AN 0")            # ERROR          division by zero

  print("\n---- check_program ----")
  check_program("HAI\nWAZZUP\n  I HAS A x ITZ 5\nBUHBYE\nVISIBLE SUM OF x AN 2\nKTHXBYE")    # output 7
  check_program("HAI\nVISIBLE y\nKTHXBYE")                                                  # ERROR y not declared
  check_program("HAI\nWAZZUP\n  I HAS A x\nBUHBYE\nGIMMEH x\nKTHXBYE")                       # gawin muna GIMMEH

def examples():
  print("\n---- sample itsura nung laman nung nodes na prinoduce ni parser ----")
  print("\nGIMMEH")
  show_ast("HAI\nWAZZUP\n  I HAS A x\nBUHBYE\nGIMMEH x\nKTHXBYE")
  print("\nIS NOW A")
  show_ast("HAI\nWAZZUP\n  I HAS A x ITZ 5\nBUHBYE\nx IS NOW A YARN\nKTHXBYE")
  print("\nO RLY?")
  show_ast("HAI\nBOTH SAEM 1 AN 1\nO RLY?\n  YA RLY\n    VISIBLE \"yes\"\n  MEBBE WIN\n    VISIBLE \"maybe\"\n  NO WAI\n    VISIBLE \"no\"\nOIC\nKTHXBYE")
  print("\nWTF?")
  show_ast("HAI\n2\nWTF?\n  OMG 1\n    VISIBLE \"one\"\n    GTFO\n  OMG 2\n    VISIBLE \"two\"\n  OMGWTF\n    VISIBLE \"other\"\nOIC\nKTHXBYE")
  print("\nIM IN YR")
  show_ast("HAI\nWAZZUP\n  I HAS A i ITZ 0\nBUHBYE\nIM IN YR lp UPPIN YR i TIL BOTH SAEM i AN 3\n  VISIBLE i\nIM OUTTA YR lp\nKTHXBYE")

def tests():
  print("\n---- test ----")
  #   check_expr("SMOOSH \"a\" AN 1 AN WIN")
  #   check_program("HAI\n...\nKTHXBYE")


if __name__ == "__main__":
  my_examples()
  examples()
  tests()