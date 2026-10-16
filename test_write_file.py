"""
write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
"""
from functions.write_file import write_file


def runTests():
    print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
    print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
    print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))

if __name__ == "__main__":
    runTests()
