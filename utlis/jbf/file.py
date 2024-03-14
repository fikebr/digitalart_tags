import os
from pathlib import Path

def scandir(dir_name):
    # https://www.geeksforgeeks.org/python-os-scandir-method/
    # https://docs.python.org/3/library/os.html#os.scandir
    # https://docs.python.org/3/library/os.html#os.DirEntry

    if isdir(dir_name):
        return os.scandir(path)
    else:
        return 0

def write_file(file, text):
    f = open(file, "w+", encoding="utf-8")
    f.write(text)
    f.close()


def isdir(dir):
    # https://docs.python.org/dev/library/pathlib.html#pathlib.Path.is_dir
    return Path(dir).is_dir()


def main():
    next

if __name__ == "__main__":
    main()
