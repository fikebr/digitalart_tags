# this is a module that contains tools that I use to manage my fooocus workflow
import os
# import re
# import json
import glob
import utlis.jbf.file as file
import utlis.jbf.bsoup as bs
import utlis.jbf.tools as tools
import utlis.jbf.toml as toml
import logging as log
import pprint

log.basicConfig(
    format="%(asctime)s %(levelname)s %(lineno)d : %(message)s",
    datefmt="%Y%m%d_%H%M%S",
    level=log.INFO,
)

pp = pprint.PrettyPrinter(indent=4)

# config
cfg = toml.load_file("config.toml")
file_tags = cfg["app"]["file_tags"]
folder = cfg["input"]["folder"]
file_extensions = cfg["app"]["image_file_extensions"]
max_files = 10000

current_pid = os.getpid()
log.info(f"the current pid: {current_pid}")


def main():
    log_file = get_log_file(folder)
    log_html = file.read_file(log_file)

    if log_file:
        log.info(f"getting all files for folder: {folder}")
        all_files = get_all_files(folder, file_extensions)
        log.info(f"{len(all_files)} files found.")
        log.info("build a file dictionary.")
        file_dict = build_file_dict(folder, all_files)

        log.info("get all toml files.")
        toml_files = get_all_toml_files(folder)
        log.info("cleaning up abandoned toml.")
        toml_files = cleanup_toml_files(folder, toml_files, file_tags)
        log.info("building a toml dictionary.")
        toml_dict = parse_existing_toml(folder, toml_files)
        log.info("getting the fooocus metadata.")
        file_dict = get_metadata(folder, file_dict, log_html, toml_dict)

        # merge toml and file dicts
        log.info("merging the file and toml metadata")
        toml_dict = merge_dictionaries(file_dict, toml_dict)

        # write toml files
        log.info("writing the toml files.")
        write_toml_files(folder, toml_dict)


def write_toml_files(folder, toml_dict):
    for name in toml_dict:
        toml_file = os.path.join(folder, f"{name}.toml")
        toml.save_file(toml_file, toml_dict[name])


def merge_dictionaries(file_dict, toml_dict):
    # the file_dict[name] will have the key "files" and maybe "fooocus"
    # the toml_dict[name] might not exist
    # the toml_dict[name] might have the key "files" and "fooocus"

    for name in file_dict:
        if name in toml_dict:
            toml_dict[name]["files"] = {}
            toml_dict[name]["files"] = file_dict[name]["files"]

            if "fooocus" in file_dict[name]:
                toml_dict[name]["fooocus"] = {}
                toml_dict[name]["fooocus"] = file_dict[name]["fooocus"]
        else:
            toml_dict[name] = file_dict[name]

    return toml_dict


def cleanup_toml_files(folder, all_toml_files, tags):
    for tfile in all_toml_files:
        (name, tags) = tools.get_tags(tfile, tags)
        fileset = glob.glob(os.path.join(folder, f"{name}*"))

        if len(fileset) == 1:
            print(f"{tfile} is an abandoned toml")
            os.remove(os.path.join(folder, tfile))

    return get_all_toml_files(folder)


def get_all_toml_files(folder: str) -> list:
    files = []
    files = files + glob.glob(os.path.join(folder, "*.toml"))
    files = map(lambda x: os.path.basename(x), files)
    return sorted(files)


def parse_existing_toml(folder: str, tomls: list) -> dict:
    toml_dict = {}
    for toml_file in tomls:
        (name, tags) = tools.get_tags(toml_file, file_tags)
        toml_dict[name] = {}
        toml_filename = os.path.join(folder, toml_file)
        log.debug(f"toml file: {toml_filename}")
        toml_dict[name] = toml.load_file(toml_filename)

    return toml_dict


def get_metadata(folder: str, d: dict, log_html: str, t: dict) -> dict:
    for name in d:
        if name not in t or "fooocus" not in t[name]:
            f = get_metadata_for_file(f"{name}.png", log_html)
            d[name]["fooocus"] = {}
            d[name]["fooocus"] = f

    return d


def get_metadata_for_file(filename, log_html):
    (name, tags) = tools.get_tags(filename, file_tags, file_extensions)

    imgfile = f"{name}.png"
    log.info(f'parsing log.html to get fooocus data for {imgfile}')
    dict = bs.metadata_from_log(log_html, imgfile)

    return dict


def build_file_dict(folder: str, all_files: list) -> dict:
    d = {}
    for file_name in all_files:
        (name, tags) = tools.get_tags(file_name, file_tags, file_extensions)
        if name not in d:
            d[name] = {}
            d[name]["files"] = {}
            d[name]["files"][file_name] = {}
            d[name]["files"][file_name]["tags"] = tags
        else:
            d[name]["files"][file_name] = {}
            d[name]["files"][file_name]["tags"] = tags

    return d


def get_all_files(folder: str, file_extensions: list) -> list:
    files = []
    for ext in file_extensions:
        files = files + glob.glob(os.path.join(folder, f"*{ext}"))

    files = map(lambda x: os.path.basename(x), files)
    return sorted(files)


def get_log_file(folder):
    log_file = os.path.join(folder, "log.html")

    # end if there is no metadata file
    if not os.path.exists(log_file):
        print("there is no metadata file to parse")
        return False
    else:
        return log_file


if __name__ == "__main__":
    main()
