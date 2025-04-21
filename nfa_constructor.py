from nfa import NFA, State, Edge
from preprocessing import preprocessing
from helpers import handle_kleene, handle_question_mark, handle_plus, handle_concatenation, handle_or

class NFAConstructor:
    def __init__(self):
        self.state_counter = 0  #state ids

    def new_state(self):
        state = State(self.state_counter)
        self.state_counter += 1
        return state

    def construct_nfa_for_literal(self, char):
        start_state = self.new_state()
        accept_state = self.new_state()
        start_state.add_edge(Edge(char, accept_state))  #transistion on char or wildcard
        nfa = NFA(self, [start_state, accept_state], start_state, [accept_state], {"S0": [("A", "S1"), ("B", "S0")]})
        return nfa

    def construct_nfa(self, regex):
        stack = []
        tokens = preprocessing(regex)  #get the postfix notation of the regex

        if not tokens:
            raise ValueError("No tokens generated from the regex.")

        for token in tokens:
            if token.isalnum():
                nfa = self.construct_nfa_for_literal(token)
                stack.append(nfa)
            elif token == '.':
                nfa = self.construct_nfa_for_literal(".")
                stack.append(nfa)
            elif token == '#':
                if len(stack) < 2:
                    raise IndexError("Not enough NFAs to concatenate.")
                nfa2 = stack.pop()
                nfa1 = stack.pop()
                nfa = handle_concatenation(nfa1, nfa2)
                stack.append(nfa)
            elif token == '|':
                if len(stack) < 2:
                    raise IndexError("Not enough NFAs to perform alternation.")
                nfa2 = stack.pop()
                nfa1 = stack.pop()
                nfa = handle_or(nfa1, nfa2)
                stack.append(nfa)
            elif token == '*':
                if len(stack) < 1:
                    raise IndexError("Not enough NFAs to apply Kleene star.")
                nfa = stack.pop()
                nfa = handle_kleene(nfa)
                stack.append(nfa)
            elif token == '?':
                if len(stack) < 1:
                    raise IndexError("Not enough NFAs to apply question mark.")
                nfa = stack.pop()
                nfa = handle_question_mark(nfa)
                stack.append(nfa)
            elif token == '+':
                if len(stack) < 1:
                    raise IndexError("Not enough NFAs to apply plus operator.")
                nfa = stack.pop()
                nfa = handle_plus(nfa)
                stack.append(nfa)

        if len(stack) != 1:
            raise ValueError(f"Unexpected number of NFAs on the stack: {len(stack)}")

        return stack.pop()
