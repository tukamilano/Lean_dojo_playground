
import subprocess
import re

#タクティック化すれば情報が得られる

def lean4_interaction(state):
    with open("current_state", mode="w") as f:
        f.write(state)
    # Start Lean in interactive mode
    command = ["lean", "--run", "./current_state"]

    # Expect the prompt
    result = subprocess.run(command, capture_output=True, text=True) #ゴールの分割の際は一番最初に解くべきゴールのみが表示される

    return result

def process_string(s):
    # "error"という文字列を含む行を削除します。
    s = "\n".join(line for line in s.split('\n') if (("error: unexpected end of input" not in line) and ("error: unsolved goals" not in line)))
    
    # 空白文字を含む最初の行を見つけ、その前の部分を取り出します。
    match = re.search(r'\n\n', s, re.MULTILINE)
    if match:
        s = s[:match.start()]
    
    return s

##tacticスタイルではない場合
#state = """
#example (α : Type) (p q : α → Prop) : (∀ x : α, p x ∧ q x) → ∀ y : α, p y :=
#  fun h : ∀ x : α, p x ∧ q x =>
#  fun y : α =>
#  by
#"""

def get_current_state(proof_so_far):
    stdout = lean4_interaction(proof_so_far).stdout
    state_so_far = process_string(stdout)
    if state_so_far == "":
        completion = "done"
    elif "error" in state_so_far:
        completion = "error"
    else:
        completion = "continue"
    return state_so_far, completion