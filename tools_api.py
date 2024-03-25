import utlis.jbf.claude as api
import utlis.jbf.file as file
import utlis.jbf.toml as toml
import os
import json
import glob
import re
import pprint
from dotenv import load_dotenv
import logging as log

log.basicConfig(
    format="%(asctime)s %(levelname)s %(lineno)d : %(message)s",
    datefmt="%Y%m%d_%H%M%S",
    level=log.INFO,
)

pp = pprint.PrettyPrinter(indent=4)

# Load the .env file
load_dotenv()
api_key = os.getenv("ANTHROPIC_KEY")

# Configuration
cfg = toml.load_file("config.toml")
file_tags = cfg["app"]["file_tags"]
folder = cfg["input"]["folder"]

def main():
    image_files = get_image_files(folder)
    image_dict = get_image_dictionary(image_files)
    image_dict = get_json_data(image_dict)
    image_dict = analyze_images(image_dict)
    # pp.pprint(image_dict)


# get all of the image files in the folder
def get_image_files(folder):
    # get image files in folder
    file_extensions = ["png", "jpg"]
    image_files = []
    for ext in file_extensions:
        image_files = image_files + glob.glob(os.path.join(folder, f"*.{ext}"))
    return image_files

def get_tags(filename):

    tags_out = []
    name = re.sub("\..+$", "", os.path.basename(filename))

    for tag in file_tags:
        if tag in name:
            tags_out.append(tag)
            name = re.sub("_" + tag, "", name)

    if tags_out:
        tag = ", ".join(tags_out)
    else:
        tag = ""

    return (name, tag)


def get_image_dictionary(image_files):

    image_d = {}

    for image_file in image_files:
        image_file = os.path.basename(image_file)
        (name, tags) = get_tags(image_file)
        tags = "orig" if tags == "" else tags

        if name not in image_d:
            image_d[name] = {}
            image_d[name]["files"] = {}

        image_d[name]["files"][tags] = image_file

        if os.path.exists(os.path.join(folder, f"{name}.json")):
            image_d[name]["files"]["json"] = f"{name}.json"

    return(image_d)

def get_json_data(image_dict):

    for name in image_dict:

        if "json" in image_dict[name]["files"]:
            # print(image_dict[name]["files"]["json"])
            image_dict[name]["json"] = {}
            image_dict[name]["json"] = load_json_file(name)

    return(image_dict)

def load_json_file(image_name):

    json_file = os.path.join(folder, f"{image_name}.json")

    with open(json_file, "r") as f:
        # Load the JSON data from the file
        data = json.load(f)

    return(data)


def analyze_images(image_dict):

    system_msg_file = os.path.abspath(os.path.dirname(__file__))
    system_msg_file = os.path.join(system_msg_file, "system_msg.txt")
    system_msg = file.read_file(system_msg_file)

    for name in image_dict:

        if "description" not in image_dict[name]:
            image_dict[name]["description"] = {}

        if "api" not in image_dict[name]["description"]:
            image_dict[name]["description"]["api"] = {}

            prompt = "no extra information available"
            if image_dict[name].get("metadata", {}).get("fooocus", {}).get("Prompt"):
                prompt = image_dict[name]["metadata"]["fooocus"]["Prompt"]

            img_file = ""
            if "thumb" in image_dict[name]["files"]:
                img_file = image_dict[name]["files"]["thumb"]
            else:
                img_file = image_dict[name]["files"]["orig"]

            img_file = os.path.join(folder, img_file)

            image_dict[name]["description"]["api"] = api.analyze_image(
                api_key, img_file, system_msg, prompt
            )
            file.write_file(os.path.join(folder, f"{name}.json"), json.dumps(image_dict[name]))

    return(image_dict)




if __name__ == "__main__":
    main()
