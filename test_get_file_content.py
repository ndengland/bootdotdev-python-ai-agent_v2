from functions.get_file_content import get_file_content


def run_tests():

    """
    get_file_content("calculator", "lorem.txt")
    """
    result = get_file_content("calculator", "lorem.txt")
    print(f"lorem.txt length: {len(result)}")
    print(f"lorem.txt truncated: {'truncated' in result}")

    """
    get_file_content("calculator", "main.py")
    get_file_content("calculator", "pkg/calculator.py")
    get_file_content("calculator", "/bin/cat") (this should return an error string)
    get_file_content("calculator", "pkg/does_not_exist.py") (this should return an error string)
    """
    print(get_file_content("calculator", "main.py"))
    print(get_file_content("calculator", "pkg/calculator.py"))
    print(get_file_content("calculator", "/bin/cat"))   # (this should return an error string)
    print(get_file_content("calculator", "pkg/does_not_exist.py"))  # (this should return an error string))

if __name__ == "__main__":
    run_tests()
