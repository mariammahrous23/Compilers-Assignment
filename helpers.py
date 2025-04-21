from nfa import NFA, Edge

EPSILON = 'ε'


def handle_kleene(nfa):
    start_state = nfa.constructor.new_state()
    accept_state = nfa.constructor.new_state()

    # add epsilon transitions from new start to old start and new accept
    start_state.add_edge(Edge(EPSILON, nfa.start_state))
    start_state.add_edge(Edge(EPSILON, accept_state))

    # add epsilon transitions from old accept to old start and new accept
    nfa.accept_states[0].add_edge(Edge(EPSILON, nfa.start_state))
    nfa.accept_states[0].add_edge(Edge(EPSILON, accept_state))

    new_nfa = NFA(nfa.constructor, [start_state, accept_state] + nfa.states, start_state, [accept_state], {"S0": [("A", "S1"), ("B", "S0")]})
    return new_nfa

def handle_question_mark(nfa):
    start_state = nfa.constructor.new_state()
    accept_state = nfa.constructor.new_state()

    # transition to either run the sub-NFA or skip directly to the new accept
    start_state.add_edge(Edge(EPSILON, nfa.start_state))
    start_state.add_edge(Edge(EPSILON, accept_state))

    # after running the sub-NFA, transition to accept
    nfa.accept_states[0].add_edge(Edge(EPSILON, accept_state))

    new_nfa = NFA(nfa.constructor, [start_state, accept_state] + nfa.states, start_state, [accept_state], {"S0": [("A", "S1"), ("B", "S0")]})
    return new_nfa

def handle_plus(nfa):
    start_state = nfa.constructor.new_state()
    accept_state = nfa.constructor.new_state()

    # must go through sub-NFA at least once
    start_state.add_edge(Edge(EPSILON, nfa.start_state))

    # allow looping from accept back to start and allow exit
    nfa.accept_states[0].add_edge(Edge(EPSILON, nfa.start_state))
    nfa.accept_states[0].add_edge(Edge(EPSILON, accept_state))

    new_nfa = NFA(nfa.constructor, [start_state, accept_state] + nfa.states, start_state, [accept_state], {"S0": [("A", "S1"), ("B", "S0")]})
    return new_nfa

def handle_concatenation(nfa1, nfa2):
    
    #linking the first's accept to the second's start
    nfa1.accept_states[0].add_edge(Edge(EPSILON, nfa2.start_state))

    new_nfa = NFA(nfa1.constructor, nfa1.states + nfa2.states, nfa1.start_state, nfa2.accept_states, {"S0": [("A", "S1"), ("B", "S0")]})
    return new_nfa


def handle_or(nfa1, nfa2):
    start_state = nfa1.constructor.new_state()
    accept_state = nfa1.constructor.new_state()

    # branch to both NFAs
    start_state.add_edge(Edge(EPSILON, nfa1.start_state))
    start_state.add_edge(Edge(EPSILON, nfa2.start_state))

    # both NFAs converge to a new accept
    nfa1.accept_states[0].add_edge(Edge(EPSILON, accept_state))
    nfa2.accept_states[0].add_edge(Edge(EPSILON, accept_state))

    new_nfa = NFA(nfa1.constructor, [start_state, accept_state] + nfa1.states + nfa2.states, start_state, [accept_state], {"S0": [("A", "S1"), ("B", "S0")]})
    return new_nfa
