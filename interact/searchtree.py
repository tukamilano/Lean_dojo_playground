from collections import deque
from transformer0 import get_tactic
from lean_dojo import *

class Node:
    def __init__(self, state=None, value=None):
        self.state = state
        self.value = value
        self.children = []
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
                self.children.append(child)
                self.actions[action] = child

def update_node_value(node): #今までに出てきたstateだったらvalueと木構造を適切に変える(考察を加える)
    if node.value is None:
        if any(child.value == 1 for child in node.children):
            node.value = 1
        elif all(child.value == -1 for child in node.children):
            node.value = -1

def breadth_first_search(root, max_nodes=100):
    node_count = 0
    queue = deque([(root, None)])

    while queue:
        if node_count >= max_nodes:
            break

        node, parent = queue.popleft()

        if node.value is None:
            actions = get_tactic(node.state.pp)
            node.generate_children(actions)
            for child in node.children:
                queue.append((child, node))
                node_count += 1            
            # Re-add parent node to the end of the queue to update its value later
            if parent is not None:
                queue.append((node, parent))
        else:
            if parent:  # If parent node exists
                update_node_value(parent)  # Update value of parent node

    if node.value is None:  # For root node
        update_node_value(node)

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

    while queue:
        node = queue.popleft()

        data.append((node.state, node.value))
        
        if node.children:
            for child in node.children:
                queue.append(child)

    return data

repo = LeanGitRepo("https://github.com/yangky11/lean4-example", "7d711f6da4584ecb7d4f057715e1f72ba175c910")
theorem = Theorem(repo, "Lean4Example.lean", "hello_world")

with Dojo(theorem) as (dojo, state):
    root = Node(state=state, value=None)
    breadth_first_search(root)
    dataset = extract_data(root)
    dataset2 = extract_data2(root)
    for data in dataset:
        print(data)
    for data in dataset2:
        print(data)
"""
actions = ['action_{}'.format(i) for i in range(3)]
root = Node(state='root', value=None)
breadth_first_search(root, actions)

dataset = extract_data(root)
for data in dataset:
    print(data)

dataset2 = extract_data2(root)
for data in dataset2:
    print(data)
"""