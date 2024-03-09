
import os
from pathlib import Path

input_folder = 'E:\Programs\Mmed\_Image\Fooocus_win64_2-0-50\Fooocus\outputs\2023-12-14'
output_folder = 'E:\Dropbox\Biz\_Inbox\tagging'

def scandir(dir_name):
    # https://www.geeksforgeeks.org/python-os-scandir-method/
    # https://docs.python.org/3/library/os.html#os.scandir
    # https://docs.python.org/3/library/os.html#os.DirEntry

    if isdir(dir_name):
        return os.scandir(path)
    else:
        return 0


def isdir(dir):
    # https://docs.python.org/dev/library/pathlib.html#pathlib.Path.is_dir
    return Path(dir).is_dir()


def main():
    next

if __name__ == "__main__":
    main()
