import string
import unittest
from preprocessing import infix_to_postfix, insert_concatenation_operators, tokenize , expand_lists

class TestRegexTokenizer(unittest.TestCase):
    def test_tokenizer_cases(self):
        test_cases = [
            ("[a-c]", ['(', 'a', '|', 'b', '|', 'c', ')']),  
            ("a(b|c)*", ['a', '(', 'b', '|', 'c', ')', '*']),
            ("[A-Z]+(abc|123)?", 
             ['(', 'A', '|', 'B', '|', 'C', '|', 'D', '|', 'E', '|', 'F', '|', 'G', '|', 'H', '|', 'I', '|', 'J', '|',
               'K', '|', 'L', '|', 'M', '|', 'N', '|', 'O', '|', 'P', '|', 'Q', '|', 'R', '|', 'S', '|', 'T', '|', 'U',
               '|', 'V', '|', 'W', '|', 'X', '|', 'Y', '|', 'Z', ')', '+', '(', 'a', 'b', 'c', '|', '1', '2', '3', ')', '?']),
            ("x.y", ['x', '.', 'y']),
            ("a|b|c", ['a', '|', 'b', '|', 'c']),
            ("([0-9])*", ['(', '(', '0', '|', '1', '|', '2', '|', '3', '|', '4', '|', '5', '|', '6', '|', '7', '|', '8', '|', '9', ')', ')', '*']),
            ("[a-c][0-9]", ['(', 'a', '|', 'b', '|', 'c', ')', '(', '0', '|', '1', '|', '2', '|', '3', '|', '4', '|', '5', '|', '6', '|', '7', '|', '8', '|', '9', ')']),
        ]
        for i, (regex, expected) in enumerate(test_cases):
            with self.subTest(f"Test case {i+1}: {regex}"):
                self.assertEqual(tokenize(regex), expected)


    def test_tokenizer_errors(self):
        error_cases = [
            "[abc",    
            "a#b",     
        ]

        for i, regex in enumerate(error_cases):
            with self.subTest(f"Error case {i+1}: {regex}"):
                with self.assertRaises(ValueError):
                    tokenize(regex)


class TestBracketExpansion(unittest.TestCase):
    def test_bracket_expansion_cases(self):
        test_cases = [
            ("[a-c]", "(a|b|c)"),
            ("[a-cx-z]", "(a|b|c|x|y|z)"),
            ("[a-c5]", "(5|a|b|c)"),
            ("[aa-bb]", "(a|b)"),  
            ("[0-2]", "(0|1|2)"),
            ("[a-zA-Z0-9]", "(" + '|'.join(
                sorted(set(
                    [chr(c) for c in range(ord('a'), ord('z')+1)] +
                    [chr(c) for c in range(ord('A'), ord('Z')+1)] +
                    [str(c) for c in range(0, 10)]
                ))
            ) + ")")
        ]

        for i, (input_expr, expected) in enumerate(test_cases):
            with self.subTest(f"Test case {i+1}: {input_expr}"):
                self.assertEqual(expand_lists(input_expr), expected)

class TestRegexProcessing(unittest.TestCase):
    
    test_cases = [
        {
            "regex": "(a|b)*abb",
            "expected_tokens": ['(', 'a', '|', 'b', ')', '*', 'a', 'b', 'b'],
            "expected_postfix": ['a', 'b', '|', '*', 'a', '.', 'b', '.', 'b' ,'.']
        },
        {
            "regex": "(a|b|c)+d(e|f)g",
            "expected_tokens": ['(', 'a', '|', 'b', '|', 'c', ')', '+', 'd', '(', 'e', '|', 'f', ')', 'g'],
            "expected_postfix": ['a', 'b', '|', 'c', '|', '+', 'd', '.', 'e', 'f', '|', '.', 'g', '.']
        },
        {
            "regex": "[a-z]ab",
            "expected_tokens": ['(', 'a', '|', 'b', '|', 'c', '|', 'd', '|', 'e', '|', 'f', '|', 'g', '|', 'h', '|', 'i', '|', 'j', '|', 'k', '|', 'l', '|', 'm', '|', 'n', '|', 'o', '|', 'p', '|', 'q', '|', 'r', '|', 's', '|', 't', '|', 'u', '|', 'v', '|', 'w', '|', 'x', '|', 'y', '|', 'z', ')', 'a', 'b'],
            "expected_postfix": ['a', 'b', '|', 'c', '|', 'd', '|', 'e', '|', 'f', '|', 'g', '|', 'h', '|', 'i', '|', 'j', '|', 'k', '|', 'l', '|', 'm', '|', 'n', '|', 'o', '|', 'p', '|', 'q', '|', 'r', '|', 's', '|', 't', '|', 'u', '|', 'v', '|', 'w', '|', 'x', '|', 'y', '|', 'z', '|', 'a', '.', 'b', '.']
        },
        {
            "regex": "(x|y|z)?abc",
            "expected_tokens": ['(', 'x', '|', 'y', '|', 'z', ')', '?', 'a', 'b', 'c'],
            "expected_postfix": ['x', 'y', '|', 'z', '|', '?', 'a', '.', 'b', '.', 'c', '.']
        },
        {
            "regex": "(a|b|c)*d+",
            "expected_tokens": ['(', 'a', '|', 'b', '|', 'c', ')', '*', 'd', '+'],
            "expected_postfix": ['a', 'b', '|', 'c', '|', '*', 'd', '+', '.']
        }
    ]
    
    def test_regex_processing(self):
        for case in self.test_cases:
            regex = case["regex"]
            expected_tokens = case["expected_tokens"]
            expected_postfix = case["expected_postfix"]            
            tokens = tokenize(regex)            
            tokens_with_concatenation = insert_concatenation_operators(tokens)
            postfix_tokens = infix_to_postfix(tokens_with_concatenation)
            self.assertEqual(tokens, expected_tokens, f"Failed for regex: {regex}")            
            self.assertEqual(postfix_tokens, expected_postfix, f"Failed for regex: {regex}")


if __name__ == "__main__":
    unittest.main()

