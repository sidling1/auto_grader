import io
import sys
import ast
import subprocess

def grade_code(file_path):
    try:
        with open(file_path, 'r') as file:
            submitted_code = file.read()

        sys.stdout = io.StringIO()
        parsed_code = ast.parse(submitted_code)
        code_obj = compile(parsed_code, "<string>", "exec")
        exec(code_obj)
        output = sys.stdout.getvalue()
        sys.stdout = sys.__stdout__

        # Coding style assessment using pycodestyle
        pycodestyle_result = subprocess.run(["pycodestyle", file_path], capture_output=True, text=True)
        if pycodestyle_result.returncode != 0:
            print("Coding Style Error:\n" + pycodestyle_result.stderr)

        # Documentation quality assessment using pydocstyle
        pydocstyle_result = subprocess.run(["pydocstyle", file_path], capture_output=True, text=True)
        if pydocstyle_result.returncode != 0:
            print("Documentation Quality Error:\n" + pydocstyle_result.stderr)

        print(f"Code executed successfully. Output: {output}")
    except FileNotFoundError as e:
        sys.stdout = sys.__stdout__
        return f"Error: File not found: {e}"
    except SyntaxError as e:
        sys.stdout = sys.__stdout__
        return f"Syntax Error: {e}"
    except Exception as e:
        sys.stdout = sys.__stdout__
        return f"Error executing code: {e}"

# Sample test case
file_path = "sample.py"
print(grade_code(file_path))