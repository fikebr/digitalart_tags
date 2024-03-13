# https://pyimagesearch.com/2024/02/12/image-processing-with-gemini-pro/
# https://aistudio.google.com/app/apikey
# https://ai.google.dev/tutorials/python_quickstart

# python -m venv venv
# venv\Scripts\activate.bat

# python.exe -m pip install --upgrade pip
# pip install -q -U google-generativeai
# pip install pillow


# [] given a folder
# [] get a list of images
# for each image...
# [] get full name, file name, image name, tags
# [] create a folder in the output folder for the image_name
# [] move all files with the same image_name to the new folder
# [] tag file with _orig
# [] create a thumbnail file
# [] use AI to get a title, tags, description
# [] 

import os
import re
import shutil
import time
from dotenv import load_dotenv

import utlis.jbf.file as file
import utlis.jbf.db as db
import utlis.jbf.gemini as api


# Load the .env file
load_dotenv()

# Access variables using os.getenv()
google_api_key = os.getenv("GOOGLE_API_KEY")



# Configuration: TODO: these should come from a config file or the command line
input_folder = 'E:/Programs/Mmed/_Image/Fooocus_win64_2-0-50/Fooocus/outputs/2024-02-21'
output_folder = 'E:/Dropbox/Biz/_Inbox/tagging'
source = 'fooocus'
dbfile = 'py_digitalart_tags.db'
image_file_extensions = ['png', 'jpg', 'svg']
ai_prompt = """For this image.
Give me a title. A description and a list of 25 keywords comma separated.
Make sure to mention the 2 primary colors, if the image represents a specific holiday or nationality, artistic style, theme and subject matter.
DO NOT mention products that the image would be good for.
DO NOT give me Additional Notes.
Use high-quality SEO keywords.

Desired format:
title: <your title here>
keywords: <your comma seperated list of 30 keywords here>
description: <your description here. on a single line>
"""
api_pasue = 3
gemini_model_vision = 'gemini-pro-vision'
gemini_model_text = 'gemini-pro'


def get_tags(filename):
    """
    Check a filename for tags at the end.
    Files that are the same after you take out the tags should be moved to the same folder.
    """

    tags = ['up2_up2_up2', 'up2_up2', 'up2', 'orig']
    tags_out = []
    name = re.sub('\..+$', '', filename)
    #print('name=', name)

    for tag in tags:
        if tag in name:
            tags_out.append(tag)
            name = re.sub('_' + tag, '', name)

    tag = ", ".join(tags_out)
    #print("tags= " + tag)

    return(name, tag)

def load_new_images(input_folder, source):

    """
        Given an input folder, load all the new image files into the db.
    """

    if file.isdir(input_folder):
        with os.scandir(input_folder) as it:
            for entry in it:
                if (
                    not entry.name.startswith(".")
                    and entry.is_file()
                    and entry.name.endswith(tuple(image_file_extensions))
                ):
                    print(entry.name.endswith())
                    tag = ''
                    (name, tag) = get_tags(entry.name)
                    db.insert_file(dbfile, source, input_folder, entry.name, tag, name)
    else:
        print("bad folder", input_folder)

def move_new_images(target_folder, dbfile):
    """
        test: does output_folder exist?
        db: query for images where status = new
        for each image
        create a target folder
        move files
        if fooocus, get the metadata from log.html
        update the db
        create the html file
    """
    if file.isdir(target_folder):

        sql = """select id, source, folder, filename, imageName from Images where status = 'New'"""
        print(sql)
        all_rows = db.queryall(dbfile, sql)
        for row in all_rows:
            # row[0] returns the first column in the query
            print('{0} : {1}, {2}, {3}, {4}'.format(row[0], row[1], row[2], row[3], row[4]))

            # make the new target dir
            newdir = '/'.join([target_folder, row[4]])
            if not file.isdir(newdir):
                os.makedirs(newdir)
            
            # get log.html            
            if row[1] == 'fooocus':
                logfile = '/'.join([row[2], 'log.html'])
                shutil.copy2(logfile, newdir) # target filename is /dst/dir/file.ext

            # move image file
            imagefile = '/'.join([row[2], row[3]])
            shutil.move(imagefile, newdir) # target filename is /dst/dir/file.ext

            # Update the db
            db.upd_img_status(dbfile, row[0], 'Moved', newdir)

    else:
        print("bad folder", target_folder)

def get_ai_description(googleapi, dbfile, prompt):
    """
        get the "Moved" images from the db and ask google gemini to give me a description
    """
    sql = """select id, source, folder, filename, imageName from Images where status = 'Moved' and (tags = '' or tags like '%orig%')"""
    print(sql)
    all_rows = db.queryall(dbfile, sql)
    for row in all_rows:
        # row[0] returns the first column in the query
        id = row[0]
        source = row[1]
        folder = row[2]
        filename = row[3]
        imageName = row[4]
        fullfilename = '/'.join([folder, filename])
        file_notes = fullfilename + '_Notes.md'
        print('{0} : {1}, {2}, {3}, {4}'.format(row[0], row[1], row[2], row[3], row[4]))

        response = api.analyze_image(google_api_key, gemini_model_vision, fullfilename, ai_prompt)
        print(response)

        write_file(file_notes, response)

        db.upd_img_notes(dbfile, id, 'Notes', response)

        time.sleep(api_pasue)

def write_file(file, text):
    f = open(file,"w+", encoding='utf-8')
    f.write(text)
    f.close()


def main():
    load_new_images(input_folder, source)
    move_new_images(output_folder, dbfile)
    get_ai_description(google_api_key, dbfile, ai_prompt)




if __name__ == "__main__":
    main()
