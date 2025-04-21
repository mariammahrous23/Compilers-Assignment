import json
from collections import defaultdict, deque
import graphviz

def read_nfa(filename):
    with open(filename) as f:
        data = json.load(f)
    start_state = data["startingState"]
    states = {}
    for k, v in data.items():
        if k != "startingState":
            states[k] = v
    return start_state, states

def epsilon_closure(nfa, states):
    stack = list(states)
    closure = set(states)

    while stack:
        state = stack.pop()
        if "ε" in nfa[state]:
            targets = nfa[state]["ε"]
            if isinstance(targets, str):
                targets = [targets]
            for t in targets:
                if t not in closure:
                    closure.add(t)
                    stack.append(t)
    return closure

def nfa_to_dfa(start_state, nfa):
    alphabet = {symbol for state in nfa.values() for symbol in state if symbol not in {"isTerminatingState", "ε"}}
    dfa = {}

    dfa_start = frozenset(epsilon_closure(nfa, [start_state]))
    queue = deque([dfa_start])
    visited = set()

    while queue:
        current = queue.popleft()
        if current in visited:
            continue
        visited.add(current)

        state_name = "_".join(sorted(current))
        dfa[state_name] = {"isTerminatingState": any(nfa[s]["isTerminatingState"] for s in current)}

        for symbol in alphabet:
            next_states = set()
            for s in current:
                if symbol in nfa[s]:
                    targets = nfa[s][symbol]
                    if isinstance(targets, str):
                        targets = [targets]
                    next_states.update(targets)

            if next_states:
                closure = epsilon_closure(nfa, next_states)
                next_state_name = "_".join(sorted(closure))
                dfa[state_name][symbol] = next_state_name

                frozen_closure = frozenset(closure)
                if frozen_closure not in visited:
                    queue.append(frozen_closure)

    return dfa_start, dfa

def minimize_dfa(start, dfa):
    final_states = {s for s, props in dfa.items() if props["isTerminatingState"]}
    non_final_states = set(dfa.keys()) - final_states
    partitions = [final_states, non_final_states]
    new_partitions = []

    def get_group(state):
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
                key = tuple((symbol, get_group(dfa[state].get(symbol))) for symbol in dfa[state] if symbol != "isTerminatingState")
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

    dot.render(filename, view=False)

def write_dfa(filename, start, dfa):
    out = {"startingState": start}
    out.update(dfa)
    with open(filename, "w") as f:
        json.dump(out, f, indent=2)

def main():
    start, nfa = read_nfa("nfa.json")
    dfa_start, dfa = nfa_to_dfa(start, nfa)
    min_start, min_dfa = minimize_dfa(dfa_start, dfa)
    write_dfa("minimized_dfa.json", min_start, min_dfa)
    draw_dfa(min_start, min_dfa)

if __name__ == "__main__":
    main()
