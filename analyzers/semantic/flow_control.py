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
  raise LOLSemanticError("gawin muna 0 RLY?")


# ======================================================================
# SWITCH-CASE (WTF?)
# ======================================================================

def execute_switch(node, scope, runtime):
  """
  Executes a switch-case statement (WTF?).
  - Compares the implicit variable IT to each OMG case literal.
  - If no OMG case matched, executes the OMGWTF default case if present.
  """
  raise LOLSemanticError("gawin muna WTF?")


# ======================================================================
# LOOPS (IM IN YR)
# ======================================================================

def execute_loop(node, scope, runtime):
  """
  Executes a loop construct (IM IN YR).
  - Handles TIL (stops when condition is WIN) and WILE (stops when condition is FAIL).
  - Applies loop operation (UPPIN or NERFIN) to the loop variable after each iteration.
  """
  raise LOLSemanticError("gawin muna IM IN YR")
