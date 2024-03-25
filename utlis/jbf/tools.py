import re
import os
import psutil


def get_memory_usage(pid):
    try:
        # Get process info using PID
        process = psutil.Process(pid)
        # Get memory info
        memory_info = process.memory_info()
        memory_usage_bytes = memory_info.rss
        if memory_usage_bytes is not None:
            # Convert bytes to megabytes for better readability (optional)
            memory_usage_mb = memory_usage_bytes / (1024 * 1024)
            return memory_usage_mb
            # print(f"Process (PID {pid}) memory usage: {memory_usage_mb:.2f} MB")

    except psutil.NoSuchProcess:
        print(f"Process with PID {pid} not found.")
        return None

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
