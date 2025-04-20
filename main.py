from nfa_constructor import NFAConstructor
import os

def generate_nfa_from_regex(regex, visualization_file, json_file, output_folder="output"):
    # Make output folder if it doesn't exist to store the png and json files
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Construct the NFA from the regex
    constructor = NFAConstructor()
    nfa = constructor.construct_nfa(regex)
    nfa.sort_and_rename_states()

    #Get the paths of the visualization and json files
    visualization_file_path = os.path.join(output_folder, visualization_file)
    json_file_path = os.path.join(output_folder, json_file)

    # Visualize the NFA and export to JSON
    nfa.visualize(visualization_file_path)
    nfa.export_to_json(json_file_path)
    
    print(f"NFA constructed for regex: {regex}")
    print(f"NFA visualization saved as {visualization_file_path}")
    print(f"NFA exported to {json_file_path}")

#Test cases
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

# Run the test cases
for idx, regex in enumerate(regexes, 1):
    visualization_file = f"nfa_visualization_{idx}"
    json_file = f"nfa_{idx}.json"
    print(f"\nTesting Regex {idx}: {regex}")
    generate_nfa_from_regex(regex, visualization_file, json_file, output_folder="output")
