from nfa_constructor import NFAConstructor
from nfa_to_dfa import read_nfa, nfa_to_dfa, minimize_dfa, draw_dfa, write_dfa
import os

def generate_nfa_and_convert_to_dfa(regex, idx, output_folder="output"):
    # Prepare paths
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    constructor = NFAConstructor()
    nfa = constructor.construct_nfa(regex)
    nfa.sort_and_rename_states()

    # File paths
    nfa_png = os.path.join(output_folder, f"nfa_visualization_{idx}")
    nfa_json = os.path.join(output_folder, f"nfa_{idx}.json")
    dfa_json = os.path.join(output_folder, f"dfa_{idx}.json")
    dfa_png = os.path.join(output_folder, f"dfa_visualization_{idx}")

    # Save NFA
    nfa.visualize(nfa_png)
    nfa.export_to_json(nfa_json)

    # Convert to DFA and minimize
    start, nfa_dict = read_nfa(nfa_json)
    dfa_start, dfa = nfa_to_dfa(start, nfa_dict)
    min_start, min_dfa = minimize_dfa(dfa_start, dfa)

    # Save Minimized DFA
    draw_dfa(min_start, min_dfa, filename=dfa_png)
    write_dfa(dfa_json, min_start, min_dfa)

    print(f"[✓] Regex: {regex}")
    print(f"    NFA saved as JSON: {nfa_json}")
    print(f"    NFA visualized: {nfa_png}.png")
    print(f"    DFA saved as JSON: {dfa_json}")
    print(f"    DFA visualized: {dfa_png}.png")

# Test regexes
regexes = [
    "(a|b)*abb",
    "ab*c+",
    "(a|b)(c|d)*e",
    "a(b|c)*d",
    "a*b*",
    "ab(c|d)*ef",
    "(a|b|c|d|e)*abc",
    "((ab|cd)*)*",
    "[a-cA-C0-3]+",               
    "a.?b",              
    "(a|.)*",            
]

# Run pipeline
for idx, regex in enumerate(regexes, 1):
    generate_nfa_and_convert_to_dfa(regex, idx)
