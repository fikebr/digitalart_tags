# this is a module that contains tools that I use to manage my fooocus workflow
import os
import re
import json
import glob
import utlis.jbf.file as file
import utlis.jbf.bsoup as bs


# config
file_tags = ["up2_up2_up2", "up2_up2", "up2", "orig"]
folder = "E:\\Programs\\Mmed\\_Image\\Fooocus_win64_2-0-50\\Fooocus\\outputs\\2024-03-14\\"
max_files = 10000


def get_metadata_for_folder(folder):
    file_extensions = ["png", "jpg"]
    log_file = f"{folder}log.html"

    # end if there is no metadata file
    if not os.path.exists(log_file):
        print("there is no metadata file to parse")
        return False

    # get image files in folder
    image_files = []
    for ext in file_extensions:
        image_files = image_files + glob.glob(f"{folder}*.{ext}")

    # filter out files that already have json files
    image_files = list(filter(lambda x: test_needs_json(x, folder), image_files))

    print(min(max_files, len(image_files)) - 1)

    for x in range(0, min(max_files, len(image_files))):
        print(f"{x} = {folder}{image_files[x]}")
        get_metadata_for_file(image_files[x], log_file)


        


def test_needs_json(file, folder):
    (name, tags) = get_tags(file)
    json_file = f"{name}.json"


    if not os.path.exists(f"{folder}{json_file}"):
        return True
    else:
        return False


def get_metadata_for_file(filename, logfile):
    (name, tags) = get_tags(filename)
    html = file.read_file(logfile)

    imgfile = f"{name}.png"
    # print(f"imgfile = {imgfile}")
    dict = bs.metadata_from_log(html, imgfile)
    if dict:
        data = {}
        data["metadata"] = {}
        data['metadata']['fooocus'] = dict
        file.write_file(f"{folder}\\{name}.json", json.dumps(data))



def get_tags(filename):
    """
    Check a filename for tags at the end.
    Files that are the same after you take out the tags should be moved to the same folder.
    """

    tags_out = []
    name = re.sub("\..+$", "", os.path.basename(filename))
    # print('name=', name)

    for tag in file_tags:
        if tag in name:
            tags_out.append(tag)
            name = re.sub("_" + tag, "", name)

    if tags_out:
        tag = ", ".join(tags_out)
    else:
        tag = ""
    # print("tags= " + tag)

    return (name, tag)


def main():
    get_metadata_for_folder(folder)


if __name__ == "__main__":
    main()
