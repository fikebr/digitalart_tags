import utlis.jbf.claude as api
import utlis.jbf.file as file
import utlis.jbf.toml as toml
import utlis.jbf.tools as tools
import os
import glob
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
image_file_extensions = cfg["app"]["image_file_extensions"]
ai_model = cfg['ai']['model']


def main():
    log.info(f"getting all files for folder: {folder}")
    image_files = get_image_files(folder, image_file_extensions)
    # pp.pprint(image_files)

    log.info("building file dictionary.")
    image_dict = get_image_dictionary(image_files)
    # pp.pprint(image_dict)

    log.info("loading existing toml data.")
    image_dict = get_toml_data(image_dict)

    log.info("Analyzing images with the help of AI.")
    log.info(f"model = {ai_model}")
    image_dict = analyze_images(image_dict, ai_model)
    # pp.pprint(image_dict)


# get all of the image files in the folder
def get_image_files(folder, image_file_extensions):
    # get image files in folder
    image_files = []
    for ext in image_file_extensions:
        image_files = image_files + glob.glob(os.path.join(folder, f"*{ext}"))
    return image_files


def get_image_dictionary(image_files):
    image_d = {}

    for image_file in image_files:
        image_file = os.path.basename(image_file)
        (name, tags) = tools.get_tags(image_file, file_tags, image_file_extensions)
        tags = "orig" if tags == "" else tags

        if name not in image_d:
            image_d[name] = {}
            image_d[name]["files"] = {}

        image_d[name]["files"][image_file] = tags

        if os.path.exists(os.path.join(folder, f"{name}.toml")):
            image_d[name]["files"][f"{name}.toml"] = "toml"

    return image_d


def get_toml_data(image_dict):
    for name in image_dict:
        if "toml" in image_dict[name]["files"]:
            # print(image_dict[name]["files"]["json"])
            # image_dict[name]["toml"] = {}
            t = load_toml_file(name)

            del t["files"]
            for key in t:
                if key in image_dict[name]:
                    image_dict[name][key] = t[key]
                else:
                    image_dict[name][key] = {}
                    image_dict[name][key] = t[key]

    return image_dict


def load_toml_file(image_name):
    toml_file = os.path.join(folder, f"{image_name}.toml")

    t = toml.load_file(toml_file)

    return t


def analyze_images(image_dict, ai_model):
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

            log.info(f"\t{name}")
            image_dict[name]["description"]["api"] = api.analyze_image(
                api_key, img_file, system_msg, prompt, ai_model
            )

            toml_file = os.path.join(folder, f"{name}.toml")
            toml.save_file(toml_file, image_dict[name])

    return image_dict


if __name__ == "__main__":
    main()
