import os
from pathlib import Path

def scandir(dir_name):
    # https://www.geeksforgeeks.org/python-os-scandir-method/
    # https://docs.python.org/3/library/os.html#os.scandir
    # https://docs.python.org/3/library/os.html#os.DirEntry

    if isdir(dir_name):
        return os.scandir(dir_name)
    else:
        return 0

def write_file(file, text):
    f = open(file, "w+", encoding="utf-8")
    f.write(text)
    f.close()


def isdir(dir):
    # https://docs.python.org/dev/library/pathlib.html#pathlib.Path.is_dir
    return Path(dir).is_dir()

def read_file(filename):
    """
    Reads the entire contents of a file and returns them as a string.

    Args:
        filename: The name of the file to read.

    Returns:
        The contents of the file as a string, or None if the file does not exist.
    """
    if os.path.exists(filename):
        try:
            with open(filename, "r") as f:
                contents = f.read()
            return contents
        except FileNotFoundError:
            # Handle the case where the file is not found
            print(f"Error: File '{filename}' not found.")
            return None
    else:
        print(f"Error: File '{filename}' does not exist.")
        return None


def main():
    next

if __name__ == "__main__":
    main()
