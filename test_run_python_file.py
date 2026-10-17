from functions.run_python_file import run_python_file


def run_tests():

    # (should print the calculator's usage instructions)
    print(run_python_file("calculator", "main.py"))

    print(run_python_file("calculator", "main.py", ["3 + 5"]))

    print(run_python_file("calculator", "tests.py"))

    # should return an error
    print(run_python_file("calculator", "../main.py"))

    # should return an error
    print(run_python_file("calculator", "nonexistent.py"))

    # should return an error
    print(run_python_file("calculator", "lorem.txt"))

if __name__ == "__main__":
    run_tests()
