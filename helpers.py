from nfa import NFA, Edge, State

EPSILON = 'ε'


def handle_kleene(nfa):
    start_state = nfa.constructor.new_state()
    accept_state = nfa.constructor.new_state()
    start_state.add_edge(Edge(EPSILON, nfa.start_state))
    start_state.add_edge(Edge(EPSILON, accept_state))
    nfa.accept_states[0].add_edge(Edge(EPSILON, nfa.start_state))
    nfa.accept_states[0].add_edge(Edge(EPSILON, accept_state))
    new_nfa = NFA(nfa.constructor, [start_state, accept_state] + nfa.states, start_state, [accept_state], {"S0": [("A", "S1"), ("B", "S0")]})
    return new_nfa


def handle_question_mark(nfa):
    start_state = nfa.constructor.new_state()
    accept_state = nfa.constructor.new_state()
    start_state.add_edge(Edge(EPSILON, nfa.start_state))
    start_state.add_edge(Edge(EPSILON, accept_state))
    nfa.accept_states[0].add_edge(Edge(EPSILON, accept_state))
    new_nfa = NFA(nfa.constructor, [start_state, accept_state] + nfa.states, start_state, [accept_state], {"S0": [("A", "S1"), ("B", "S0")]})
    return new_nfa


def handle_plus(nfa):
    start_state = nfa.constructor.new_state()
    accept_state = nfa.constructor.new_state()
    start_state.add_edge(Edge(EPSILON, nfa.start_state))
    nfa.accept_states[0].add_edge(Edge(EPSILON, nfa.start_state))
    nfa.accept_states[0].add_edge(Edge(EPSILON, accept_state))
    new_nfa = NFA(nfa.constructor, [start_state, accept_state] + nfa.states, start_state, [accept_state], {"S0": [("A", "S1"), ("B", "S0")]})
    return new_nfa


def handle_concatenation(nfa1, nfa2):
    nfa1.accept_states[0].add_edge(Edge(EPSILON, nfa2.start_state))
    new_nfa = NFA(nfa1.constructor, nfa1.states + nfa2.states, nfa1.start_state, nfa2.accept_states, {"S0": [("A", "S1"), ("B", "S0")]})
    return new_nfa


def handle_or(nfa1, nfa2):
    start_state = nfa1.constructor.new_state()
    accept_state = nfa1.constructor.new_state()
    start_state.add_edge(Edge(EPSILON, nfa1.start_state))
    start_state.add_edge(Edge(EPSILON, nfa2.start_state))
    nfa1.accept_states[0].add_edge(Edge(EPSILON, accept_state))
    nfa2.accept_states[0].add_edge(Edge(EPSILON, accept_state))
    new_nfa = NFA(nfa1.constructor, [start_state, accept_state] + nfa1.states + nfa2.states, start_state, [accept_state], {"S0": [("A", "S1"), ("B", "S0")]})
    return new_nfa
