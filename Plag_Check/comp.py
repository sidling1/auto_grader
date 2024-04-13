import difflib

def preprocess_line(line):
    # Remove spaces, convert to lowercase, and ignore tab spacing
    return line.replace(' ', '').lower().replace('\t', '')

def compare_files(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        content1 = f1.readlines()
        content2 = f2.readlines()

    # Preprocess lines
    content1 = [preprocess_line(line) for line in content1]
    content2 = [preprocess_line(line) for line in content2]

    # Compare the files using difflib
    diff = difflib.ndiff(content1, content2)

    matching_lines = 0
    neg_lines = 0
    for line in diff:
        if line.startswith('  '):
            print(line)
            matching_lines += 1
        elif line.startswith('- '):
            neg_lines += 1

    # Calculate plagiarism percentage
    total_lines = len(content1)
    plagiarism_percentage = (matching_lines / total_lines) * 100

    print(f'The files {file1} and {file2} are {plagiarism_percentage}% plagiarized.')

# Usage
file1 = 'file1.py'
file2 = 'file2.py'

compare_files(file1, file2)
