import json
import graphviz

EPSILON = 'ε'


class Edge:
    def __init__(self, symbol, to_state):
        self.symbol = symbol
        self.to_state = to_state

    def __repr__(self):
        return f"({self.symbol}, {self.to_state.state_id})"


class State:
    def __init__(self, state_id):
        self.state_id = state_id
        self.outgoing_edges = []
        self.label = str(state_id)

    def add_edge(self, edge):
        self.outgoing_edges.append(edge)

    def __repr__(self):
        return f"State({self.state_id}, {self.outgoing_edges})"

    def __lt__(self, other):
        return self.state_id < other.state_id


class NFA:
    def __init__(self, constructor, states, start_state, accept_states, transitions):
        self.constructor = constructor
        self.states = states
        self.start_state = start_state
        self.accept_states = accept_states
        self.transitions = transitions
        self.final_state = accept_states[0]
        self.states_sorted = False
        self.sorted_states = []

    def sort_and_rename_states(self):
        self.sorted_states = sorted(self.states)
        self.states_sorted = True

    def export_to_json(self, file_path=None):
        if not self.states_sorted:
            raise ValueError("States are not sorted. Call `sort_and_rename_states` before exporting to JSON.")

        outputJson = dict()
        outputJson["startingState"] = self.start_state.label

        for stat in self.states:
            stateDict = dict()

            if stat == self.accept_states[0]:
                stateDict["isTerminatingState"] = True
            else:
                stateDict["isTerminatingState"] = False

            for edg in stat.outgoing_edges:
                if edg.symbol in stateDict:
                    if isinstance(stateDict[edg.symbol], list):
                        stateDict[edg.symbol].append(edg.to_state.label)
                    else:
                        stateDict[edg.symbol] = [stateDict[edg.symbol], edg.to_state.label]
                else:
                    stateDict[edg.symbol] = edg.to_state.label

            outputJson[stat.label] = stateDict

        if file_path:
            with open(file_path, 'w', encoding="utf-8") as nfaOutFile:
                json.dump(outputJson, nfaOutFile, indent=6, ensure_ascii=False)
        else:
            return outputJson 

    def visualize(self, file_path):
        gra = graphviz.Digraph(graph_attr={'rankdir': 'LR'})

        for stat in self.states:
            label = stat.label
            if stat == self.start_state:
                gra.node("", _attributes={'shape': 'none'})
                gra.edge("", stat.label)

            if stat == self.accept_states:
                gra.node(stat.label, _attributes={'peripheries': '2', 'color': 'green', 'style': 'filled', 'fillcolor': 'lightgreen'})
            elif stat == self.final_state:
                gra.node(stat.label, _attributes={'shape': 'doublecircle', 'color': 'red', 'style': 'dashed', 'fillcolor': 'lightcoral'})
            else:
                gra.node(stat.label, _attributes={'shape': 'circle', 'color': 'black', 'style': 'filled', 'fillcolor': 'gray'})

        for stat in self.states:
            for edg in stat.outgoing_edges:
                gra.edge(stat.label, edg.to_state.label, label=edg.symbol)

        gra.format = 'png'
        gra.render(file_path, view=False, cleanup=True)
        return gra.source
