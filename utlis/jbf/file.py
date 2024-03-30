import os
import glob
import shutil
from pathlib import Path

def scandir(dir_name: str, patterns = []) -> list:
    # https://www.geeksforgeeks.org/python-os-scandir-method/
    # https://docs.python.org/3/library/os.html#os.scandir
    # https://docs.python.org/3/library/os.html#os.DirEntry

    if not patterns:
        patterns = ["*.*"]

    if isdir(dir_name):
        files = []
        for ext in patterns:
            files = files + glob.glob(os.path.join(dir_name, ext))

        files = list(map(lambda x: os.path.basename(x), files))
        return sorted(files)
    else:
        return 0

def write_file(file, text):
    f = open(file, "w", encoding="utf-8")
    f.write(text)
    f.close()


def copy_file(source, dest):
    shutil.copyfile(source, dest)


def isdir(dir):
    # https://docs.python.org/dev/library/pathlib.html#pathlib.Path.is_dir
    return Path(dir).is_dir()

def read_file(filename):
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
