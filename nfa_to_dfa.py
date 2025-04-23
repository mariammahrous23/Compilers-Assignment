import json
from collections import defaultdict, deque
import graphviz

def read_nfa(filename):
    with open(filename) as file:
        states_data = json.load(file)
    start_state = states_data["startingState"]
    states = {}
    for index, state in states_data.items():
        if index != "startingState":
            states[index] = state
    return start_state, states

def epsilon_closure(nfa, state):
    stack = list(state)
    closure = set(state)
    while stack: #loop until emptying the stack
        state_in_test = stack.pop()
        if "ε" in nfa[state_in_test]:            #if exists ε transition
            targets = nfa[state_in_test]["ε"]    #states reachable via ε
            if isinstance(targets, str): #if one item, wrap it for iteration
                targets = [targets]
            for t in targets:
                if t not in closure:
                    closure.add(t)
                    stack.append(t) #examine for further states
    return closure

def nfa_to_dfa(start_state, nfa):
    # Extract input symbols
    input_symbols = set()
    for state in nfa.values():                # Loop over each state's dictionary
        for symbol in state:                  # Loop over the keys in that state's transitions
            if symbol not in {"isTerminatingState", "ε"}:
                input_symbols.add(symbol)   

    dfa = {}
    dfa_start = frozenset(epsilon_closure(nfa, [start_state])) # All states that can be accessed by epsilon from start state
    queue = deque([dfa_start])
    visited = set()

    while queue:
        # mark the visisted state
        current = queue.popleft()
        if current in visited:
            continue
        visited.add(current)

        state_name = "_".join(sorted(current)) #readable state name e.g. 2_4_5_7

        # mark the state as isTerminatingState if so
        is_terminating = False
        for s in current:
            if nfa[s]["isTerminatingState"]:
                is_terminating = True
                break  # No need to check further — one terminating NFA state is enough
        dfa[state_name] = {"isTerminatingState": is_terminating}

        # Gather all states reachable by a symbol e.g. (a, b, .) from current state
        for symbol in input_symbols:
            next_states = set()
            for s in current:
                if symbol in nfa[s]: # If s has a transition on symbol, add the target(s) to next_states
                    targets = nfa[s][symbol]
                    if isinstance(targets, str):
                        targets = [targets]
                    next_states.update(targets)

            if next_states:
                closure = epsilon_closure(nfa, next_states)
                next_state_name = "_".join(sorted(closure))
                dfa[state_name][symbol] = next_state_name # update the transition

                frozen_closure = frozenset(closure) # frozen set to use as dictionary keys
                if frozen_closure not in visited: # if new state
                    queue.append(frozen_closure)

    return dfa_start, dfa

def minimize_dfa(start, dfa):
    final_states = set()
    for state_name, props in dfa.items():
        if props["isTerminatingState"]:
            final_states.add(state_name)

    non_final_states = set(dfa.keys()) - final_states
    partitions = [final_states, non_final_states]
    new_partitions = []

    def get_group(state): # Returns the index of the partition that a state belongs to
        for i, group in enumerate(partitions):
            if state in group:
                return i
        return -1

    changed = True
    while changed:
        changed = False
        new_partitions = []

        for group in partitions:
            split_map = defaultdict(set)
            for state in group:
                key_parts = []  # temporary list to hold (symbol, group_index) pairs
                for symbol in dfa[state]:
                    if symbol != "isTerminatingState":
                        target_state = dfa[state].get(symbol)  # the state that `state` transitions to on this symbol
                        group_index = get_group(target_state)  # the group index that target_state belongs to
                        key_parts.append((symbol, group_index))  # append the pair to the list
                key = tuple(key_parts)  # convert list to tuple
                split_map[key].add(state)
            new_partitions.extend(split_map.values())
            if len(split_map) > 1:
                changed = True

        partitions = new_partitions

    state_map = {}
    for i, group in enumerate(partitions):
        name = f"M{i}"
        for state in group:
            state_map[state] = name

    minimized_dfa = {}
    for group in partitions:
        rep = next(iter(group))
        name = state_map[rep]
        minimized_dfa[name] = {
            "isTerminatingState": dfa[rep]["isTerminatingState"]
        }
        for symbol in dfa[rep]:
            if symbol == "isTerminatingState":
                continue
            minimized_dfa[name][symbol] = state_map[dfa[rep][symbol]]

    minimized_start = state_map["_".join(sorted(start))]
    return minimized_start, minimized_dfa

def draw_dfa(start, dfa, filename="dfa_graph"):
    dot = graphviz.Digraph(format="png")
    dot.attr(rankdir='LR')

    for state, props in dfa.items():
        shape = "doublecircle" if props["isTerminatingState"] else "circle"
        dot.node(state, shape=shape)

    dot.node("", shape="none")
    dot.edge("", start)

    for state, props in dfa.items():
        for symbol, target in props.items():
            if symbol == "isTerminatingState":
                continue
            dot.edge(state, target, label=symbol)

    dot.render(filename, view=False, cleanup=True)

def write_dfa(filename, start, dfa):
    out = {"startingState": start}
    out.update(dfa)
    with open(filename, "w") as f:
        json.dump(out, f, indent=2)
