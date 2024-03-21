import re
import os

def get_tags(filename, tags):
    tags_out = []
    name = re.sub("\..+$", "", os.path.basename(filename))

    for tag in tags:
        if tag in name:
            tags_out.append(tag)
            name = re.sub("_" + tag, "", name)

    if tags_out:
        tag = ", ".join(tags_out)
    else:
        tag = ""

    return (name, tag)
