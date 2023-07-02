from repl_lean4 import get_current_state
from transformer import get_tactic
from queue import Queue

#Few shot使ってみてもいいかも
initial_proof = """
example (p q : Prop) : p ∨ q → q ∨ p := by
"""

def prove(proof):
    proof_stack = Queue(100)
    proof_stack.put({"proof": proof, "last_state": ""})
    while not proof_stack.empty():
        proof_and_last_state = proof_stack.get()

        proof = proof_and_last_state["proof"]
        last_state = proof_and_last_state["last_state"]

        state, completion = get_current_state(proof)
        if completion == "done":
            return proof
        elif (completion == "error") or (state == last_state):
            pass
        else:
            print(proof)
            tactic_candidates = get_tactic(state)
            for tactic in tactic_candidates:
                proof_stack.put({"proof": proof + tactic + "\n", "last_state": state})

def main():
    print(prove(initial_proof))

if __name__ == "__main__":
    main()
