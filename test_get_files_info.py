from functions import get_files_info

def runTests():

    print(get_files_info.get_files_info("calculator", "."))
    print(get_files_info.get_files_info("calculator", "/bin"))
    print(get_files_info.get_files_info("calculator", "../"))
    print(get_files_info.get_files_info("calculator", "main.py"))


if __name__ == "__main__":
    runTests()
