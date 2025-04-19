from nfa_constructor import NFAConstructor
regex = "(a|b)*abb"
constructor = NFAConstructor()
nfa = constructor.construct_nfa(regex)

nfa.sort_and_rename_states()

nfa.visualize("nfa_visualization")
nfa.export_to_json("nfa.json")
