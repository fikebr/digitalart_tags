import re
import os


def get_tags(filename: str, tags: list, img_files_exts: list = "") -> list:
    tags_out = []
    name = re.sub("\..+$", "", os.path.basename(filename))

    ext = os.path.splitext(filename)[1]
    is_img = 1
    if ext not in img_files_exts:
        is_img = 0

    for tag in tags:
        if tag in name:
            tags_out.append(tag)
            name = re.sub("_" + tag, "", name)

    if ext == ".toml":
        tags_out.append('toml')

    if tags_out:
        tag = ", ".join(tags_out)
    else:
        tag = ""

    if not tag and is_img:
        tag = "orig"

    return (name, tag)
