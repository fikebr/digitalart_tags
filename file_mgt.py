# given a folder
# get a list of images
# for each image...
# get full name, file name, image name, tags
# create a folder in the output folder for the image_name
# move all files with the same image_name to the new folder
# tag file with _orig
# create a thumbnail file

import os
import utlis.jbf.file as file




input_folder = 'E:\Programs\Mmed\_Image\Fooocus_win64_2-0-50\Fooocus\outputs\2023-12-14'
output_folder = 'E:\Dropbox\Biz\_Inbox\tagging'

def my_scandir(dir_name):
    # https://www.geeksforgeeks.org/python-os-scandir-method/
    # https://docs.python.org/3/library/os.html#os.scandir
    # https://docs.python.org/3/library/os.html#os.DirEntry

    os.path.isdir('new_folder')
    obj = os.scandir(path)



def main():
    print(file.isdir(input_folder))
    obj = file.scandir(input_folder)
    



if __name__ == "__main__":
    main()
