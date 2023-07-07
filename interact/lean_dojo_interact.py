#目標　mathlib datasetで強化学習させるコードを書く
from lean_dojo import *
from transformer0 import get_tactic
from searchtree import breadth_first_search, Node

repo = LeanGitRepo("https://github.com/yangky11/lean4-example", "7d711f6da4584ecb7d4f057715e1f72ba175c910")
theorem = Theorem(repo, "Lean4Example.lean", "hello_world")

with Dojo(theorem) as (dojo, state):
    root = Node(state=state, value=None)
    breadth_first_search(root)
    #state_action_dataset = extract_data(root)
    #state_dataset = extract_data2(root)

"""
def prove_and_get_current_state(theorem):
  with Dojo(theorem) as (dojo, state):
    dataset = []
    proof_stack = Queue(100)
    print(state)
    tactic = get_tactic(state.pp)
    print(tactic)
   
    state = dojo.run_tac(state, tactic)
    print(isinstance(state, ProofFinished))
    print(isinstance(state, TacticError))
    print(state)

def get_current_state(state, tactic):
    new_state = dojo.run_tac(state, tactic)
    if isinstance(new_state, ProofFinished):
        return {"state": state, "tactic": tactic, "reward": 1}
    elif (isinstance(new_state, TacticError)) or (new_state == state):
        return {"state": state, "tactic": tactic, "reward": -1}
    else:
       
"""     