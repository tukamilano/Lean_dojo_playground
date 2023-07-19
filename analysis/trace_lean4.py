import xml.etree.ElementTree as ET

# Reload and parse the XML file
tree = ET.parse('./traceanalysis.xml')
root = tree.getroot()

# Initialize empty dictionaries to store state-tactic and state-premise pairs
state_tactic_pairs = {}
state_premise_pairs = {}

# Then, parse each TacticNode
for node in root.iter('TacticNode'):
    state = node.attrib.get('state_before', '')
    tactic = node.attrib.get('tactic', '')

    # Store the state-tactic pair
    if state not in state_tactic_pairs:
        state_tactic_pairs[state] = []
    state_tactic_pairs[state].append(tactic)

    # Store the state-premise pairs
    if state not in state_premise_pairs:
        state_premise_pairs[state] = []
    for ident in node.iter('IdentNode'):
        full_name = ident.attrib.get('full_name', '')
        if full_name:  # Only add the full_name if it is not empty
            state_premise_pairs[state].append(full_name)

# Get the first few state-tactic and state-premise pairs for verification
first_state_tactic_pairs = list(state_tactic_pairs.items())
first_state_premise_pairs = list(state_premise_pairs.items())

print(first_state_tactic_pairs)
print(first_state_premise_pairs)
