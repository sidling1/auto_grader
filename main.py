import re
from difflib import SequenceMatcher

def tokenize(code):
    # Remove comments before tokenizing
    code = re.sub(r'//.*?\n|/\*.*?\*/', '', code, flags=re.DOTALL)
    # Tokenize the code using regular expressions
    return re.findall(r'\b\w+\b', code)

def compare_code(code1, code2):
    tokens1 = tokenize(code1)
    tokens2 = tokenize(code2)

    # Compare token lists
    similarity_ratio = SequenceMatcher(None, tokens1, tokens2).ratio()
    return similarity_ratio

def main():
    # Read two C code files
    with open("code1.c", "r") as file:
        code1 = file.read()

    with open("code2.c", "r") as file:
        code2 = file.read()

    # Compare the codes
    similarity_ratio = compare_code(code1, code2)

    print("Similarity Ratio:", similarity_ratio)

if __name__ == "__main__":
    main()
