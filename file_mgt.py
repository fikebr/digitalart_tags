import os
import re
import shutil
import time
import toml
from dotenv import load_dotenv

import utlis.jbf.file as file
import utlis.jbf.db as db
import utlis.jbf.gemini as api

# TODO: tag file with _orig
# TODO: create a thumbnail file
# TODO: write metadata for 

## Notes
# https://pyimagesearch.com/2024/02/12/image-processing-with-gemini-pro/
# https://aistudio.google.com/app/apikey
# https://ai.google.dev/tutorials/python_quickstart

# python -m venv venv
# venv\Scripts\activate.bat

# python.exe -m pip install --upgrade pip
# pip install -q -U google-generativeai
# pip install pillow

# Load the config file
cfg = toml.load("config.toml")

# Load the .env file
load_dotenv()

# Access variables using os.getenv()
cfg["ai"]["google_api_key"] = os.getenv("GOOGLE_API_KEY")


def get_tags(filename):
    """
    Check a filename for tags at the end.
    Files that are the same after you take out the tags should be moved to the same folder.
    """

    tags_out = []
    name = re.sub('\..+$', '', filename)
    #print('name=', name)

    for tag in cfg["app"]["file_tags"]:
        if tag in name:
            tags_out.append(tag)
            name = re.sub('_' + tag, '', name)

    tag = ", ".join(tags_out)
    #print("tags= " + tag)

    return(name, tag)

def load_new_images(input_folder, source, dbfile, image_file_extensions):

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

        id = row[0]
        folder = row[2]
        filename = row[3]
        fullfilename = '/'.join([folder, filename])
        file_notes = fullfilename + '_Notes.md'
        print('{0} : {1}, {2}, {3}, {4}'.format(row[0], row[1], row[2], row[3], row[4]))

        ai_description = api.analyze_image(
            googleapi, cfg['ai']['gemini']['models']['vision'], fullfilename, cfg['prompts']['ai_prompt']
        )
        # print(response)

        parsed = api.parse_description(
            googleapi,
            cfg["ai"]["gemini"]["models"]["text"],
            cfg["prompts"]["ai_prompt_parse"],
            ai_description,
            cfg["prompts"]["ai_prompt_parse_parts"],
        )

        db.upd_img_notes(dbfile, id, "Notes", ai_description, parsed)

        file.write_file(file_notes, ai_description)

        time.sleep(cfg['ai']['api_pasue'])




def main():
    load_new_images(
        cfg["input"]["folder"],
        cfg["input"]["source"],
        cfg["db"]["file"],
        cfg["app"]["image_file_extensions"],
    )
    move_new_images(cfg["output"]["folder"], cfg["db"]["file"])
    get_ai_description(cfg["ai"]["google_api_key"], cfg["db"]["file"], cfg['prompts']['ai_prompt'])
    pass




if __name__ == "__main__":
    main()
