# this is a module that contains tools that I use to manage my fooocus workflow
import os
# import re
# import json
import glob
import pprint
import utlis.jbf.file as file
import utlis.jbf.bsoup as bs
import utlis.jbf.tools as tools
import utlis.jbf.toml as toml

pp = pprint.PrettyPrinter(indent=4)

# config
cfg = toml.load_file("config.toml")
file_tags = cfg['app']['file_tags']
folder = cfg['input']['folder']
file_extensions = cfg["app"]["image_file_extensions"]
max_files = 10000

def main():
    log_file = get_log_file(folder)

    if log_file:
        all_files = get_all_files(folder, file_extensions)
        file_dict = build_file_dict(folder, all_files)
        # file_dict = parse_existing_toml(folder, file_dict)
        file_dict = get_metadata(folder, file_dict, log_file)
        pp.pprint(file_dict)

def parse_existing_toml(folder: str, d: dict) -> dict:
    for name in d:
        for file_name in d[name]['files']:
            if "toml" in d[name]["files"][file_name]["tags"]:
                t = toml.load_file(os.path.join(folder, file_name))

    return(d)

def get_metadata(folder: str, d: dict, logfile: str) -> dict:
    for name in d:
        if 'fooocus' not in d[name]:
            f = get_metadata_for_file(f"{name}.png", logfile)
            d[name]['fooocus'] = {}
            d[name]["fooocus"] = f

    return d

def get_metadata_for_file(filename, logfile):
    (name, tags) = tools.get_tags(filename, file_tags, file_extensions)
    html = file.read_file(logfile)

    imgfile = f"{name}.png"
    # print(f"imgfile = {imgfile}")
    dict = bs.metadata_from_log(html, imgfile)

    return(dict)

def build_file_dict(folder: str, all_files: list) -> dict:
    d = {}
    for file_name in all_files:
        (name, tags) = tools.get_tags(file_name, file_tags, file_extensions)
        if name not in d:
            d[name] = {}
            d[name]['files'] = {}
            d[name]["files"][file_name] = {}
            d[name]["files"][file_name]["tags"] = tags
    return(d)


def get_all_files(folder: str, file_extensions: list) -> list:
    file_extensions.append('json')
    file_extensions.append('toml')

    files = []
    for ext in file_extensions:
        files = files + glob.glob(os.path.join(folder, f"*{ext}"))

    files = map(lambda x: os.path.basename(x), files)
    return(sorted(files))

def get_log_file(folder):
    log_file = os.path.join(folder, "log.html")

    # end if there is no metadata file
    if not os.path.exists(log_file):
        print("there is no metadata file to parse")
        return(False)
    else:
        return(log_file)


if __name__ == "__main__":
    main()
