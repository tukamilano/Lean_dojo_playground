from collections import deque
from transformer0 import get_tactic
from lean_dojo import *

class Node:
    def __init__(self, state=None, value=None):
        self.state = state
        self.value = value
        self.children = []
        self.parents = []  # Add a list of parent nodes
        self.actions = {}

    def generate_children(self, actions):
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

def breadth_first_search(root, max_nodes=5):
    node_count = 0
    visited_states = set()
    queue = deque([root])

    while queue:
        node = queue.popleft()

        if node.value is None and node.state not in visited_states:
            actions = get_tactic(node.state.pp)
            node.generate_children(actions)
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

repo = LeanGitRepo("https://github.com/yangky11/lean4-example", "7d711f6da4584ecb7d4f057715e1f72ba175c910")
theorem = Theorem(repo, "Lean4Example.lean", "hello_world") 
# mathlibのtheoremを全て収集したい
"""
repo = LeanGitRepo("https://github.com/leanprover-community/mathlib4", "b342a33cff014bf01c918fe0199362c23566510c")
theorem = Theorem(repo, "Mathlib/Data/Bool/Basic.lean", "exists_bool")
"""
with Dojo(theorem) as (dojo, state):
    root = Node(state=state, value=None)
    breadth_first_search(root)
    # state, action, next_state, reward
    dataset = extract_data(root)
    # state, reward
    dataset2 = extract_data2(root)
    for data in dataset:
        print(data)
    for data in dataset2:
        print(data)