# 1. mathlibの全ての定理を収集する
# 2. 言語モデルの強化学習を行う

from collections import deque
from transformer1 import train
from transformer0 import get_tactic
from lean_dojo import *

class Node:
    def __init__(self, state=None, value=None):
        self.state = state
        self.value = value
        self.children = []
        self.parents = []  # Add a list of parent nodes
        self.actions = {}

    def generate_children(self, actions, dojo):
        if self.value is None:
            for action in actions:
                child_state = dojo.run_tac(self.state, action)
                if isinstance(child_state, ProofFinished):
                    val = 1
                elif isinstance(child_state, TacticError):
                    val = -1
                else:
                    val = None

                child = Node(child_state, val)
                child.parents.append(self)  # Add this node as a parent of the child
                self.children.append(child)
                self.actions[action] = child

def breadth_first_search(root, dojo, max_nodes=5):
    node_count = 0
    visited_states = set()
    queue = deque([root])

    while queue:
        node = queue.popleft()

        if node.value is None and node.state not in visited_states:
            actions = get_tactic(node.state.pp)
            node.generate_children(actions, dojo)
            visited_states.add(node.state)
            node_count += 1 

        if node.value is None and not isinstance(node.state, TacticError):
            update_node_value(node)

        if node_count >= max_nodes:
            break

        for child in node.children:
            if child.state not in visited_states:
                queue.append(child)

def update_node_value(node):
    if node.value is None:
        if any(child.value == 1 for child in node.children):
            node.value = 1
        elif all(child.value == -1 for child in node.children) or any(parent.state == node.state for parent in node.parents):
            node.value = -1

    return node.value

def extract_data(root):
    data = []
    queue = deque([root])

    while queue:
        node = queue.popleft()

        for action, child in node.actions.items():
            data.append((node.state, action, child.state, child.value))
            if child.children:
                queue.append(child)

    return data

def extract_data2(root):
    data = []
    queue = deque([root])
    visited_states = set()

    while queue:
        node = queue.popleft()

        if node.state not in visited_states:
            data.append((node.state, node.value))
            visited_states.add(node.state)

            if node.children:
                for child in node.children:
                    if child.state not in visited_states:
                        queue.append(child)
    return data
"""
# mathlibのtheoremを全て収集したい(こういうことするよりカリキュラムラーニングさせる方が意味あるかも)
def benchmark():
    with open("/Users/milano/Downloads/leandojo_benchmark_4/random/train.json", "r") as json_file:
        objects = json.load(json_file)

    path_name = []
    for object in objects:
        path_name.append(object['file_path'],object['full_name'])

repo = LeanGitRepo("https://github.com/yangky11/lean4-example", "7d711f6da4584ecb7d4f057715e1f72ba175c910")
theorem = Theorem(repo, path_name[i][0], path_name[i][1]) 
"""
repo = LeanGitRepo("https://github.com/yangky11/lean4-example", "7d711f6da4584ecb7d4f057715e1f72ba175c910")
theorem = Theorem(repo, "Lean4Example.lean", "hello_world") 
"""
repo = LeanGitRepo("https://github.com/leanprover-community/mathlib4", "5ad453cbd11b75f8b69df927eb1b2c98e7adabdc")
theorem = Theorem(repo, "Mathlib/Data/Bool/Basic.lean", "Bool.exists_bool")
"""
def generate_dataset(theorem):
    dojo, state = Dojo(theorem).__enter__()
    root = Node(state=state, value=None)
    breadth_first_search(root, dojo) #HTPSに置き換え可能
    # state, action, next_state, reward
    dataset = extract_data(root)
    # state, reward
    dataset2 = extract_data2(root)
    return dataset, dataset2

dataset, dataset2 = generate_dataset(theorem)

for data in dataset:
    print(data)

train(dataset)
