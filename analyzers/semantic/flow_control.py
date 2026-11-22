#==================================================================
# Executes conditionals (O RLY?), switch cases (WTF?), and loops (IM IN YR)
#==================================================================
from analyzers.semantic.errors import LOLSemanticError,  BreakSignal
from analyzers.semantic.typecast import to_troof, to_num
from analyzers.semantic.expressions import evaluate_expression, values_equal
from analyzers.semantic import statements

MAX_LOOP_ITERATIONS = 10000

# ======================================================================
# IF-THEN CONDITIONAL (O RLY?)
# ======================================================================

def execute_if_then(node, scope, runtime):
  """
  Executes an if-then structure (O RLY?).
  - Checks implicit variable IT:
    - If IT is WIN (truthy via to_troof), execute ya_rly branch.
    - If none matched, execute no_wai (else) branch if present.
  """

  # if IT is true, run YA RLY
  if to_troof(scope["IT"]):
    statements.execute_code_block(node["ya_rly"], scope, runtime)
    return

  # else, check each MEBBE
  for mebbe in node["mebbes"]:
    runtime["line"] = mebbe.get("line", node["line"])

    if to_troof(evaluate_expression(mebbe["condition"], scope, runtime)):
      statements.execute_code_block(mebbe["body"], scope, runtime)
      return

  if node["no_wai"] is not None:
    statements.execute_code_block(node["no_wai"], scope, runtime)


  # raise LOLSemanticError("gawin muna 0 RLY?")


# ======================================================================
# SWITCH-CASE (WTF?)
# ======================================================================

def execute_switch(node, scope, runtime):
  """
  Executes a switch-case statement (WTF?).
  - Compares the implicit variable IT to each OMG case literal.
  - If no OMG case matched, executes the OMGWTF default case if present.
  """

  it_val = scope["IT"]
  cases = node["cases"]

  start = None

  # find index of first OMG
  for i, case in enumerate(cases):
    runtime["line"] = case.get("line", node["line"])
    case_val = evaluate_expression(case["value"], scope, runtime)

    if values_equal(it_val, case_val):
      start = i
      break

  try:
    if start is not None:
      # run matched case
      for case in cases[start:]:
        statements.execute_code_block(case["body"], scope, runtime)

    # run default case if nothing matched
    if node["default"] is not None:
      statements.execute_code_block(node["default"], scope, runtime)

  except BreakSignal:
    pass #ends pag GTFO na

  # raise LOLSemanticError("gawin muna WTF?")


# ======================================================================
# LOOPS (IM IN YR)
# ======================================================================

def execute_loop(node, scope, runtime):
  """
  Executes a loop construct (IM IN YR).
  - Handles TIL (stops when condition is WIN) and WILE (stops when condition is FAIL).
  - Applies loop operation (UPPIN or NERFIN) to the loop variable after each iteration.
  """

  var = node["var"]
  op = node["op"]
  cond = node["cond"]
  iterations = 0
  
  runtime["line"] = node["line"]
  statements.check_declared(var, scope)
  
  while True:
    iterations += 1

    if iterations > MAX_LOOP_ITERATIONS:
      runtime["line"] = node["line"]
      raise LOLSemanticError(f"loop '{node['label']}' exceeded {MAX_LOOP_ITERATIONS} iterations.")

    runtime["line"] = node["line"]


    # check loop cond (if wala, skip)
    if cond is not None:
      result = to_troof(evaluate_expression(cond["expr"], scope, runtime))

      if cond["kind"] == "TIL" and result: #stop when WIN
        break

      if cond["kind"] == "WILE" and not result: #stop when FAIL
        break


    # run the body
    try:
      statements.execute_code_block(node["body"], scope, runtime)
    except BreakSignal:
      break


    # apply UPPIN/NERFIN to loop var
    runtime["line"] = node["line"]
    statements.check_declared(var, scope)
    
    curr = to_num(scope[var])
    if op == "UPPIN":
      scope[var] = curr + 1

    elif op == "NERFIN":
      scope[var] = curr - 1

    else:
      raise LOLSemanticError(f"Unknown loop operation '{op}'")

  # raise LOLSemanticError("gawin muna IM IN YR")
