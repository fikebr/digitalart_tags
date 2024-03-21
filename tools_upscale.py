import glob
import os
import pprint
import subprocess

import utlis.jbf.tools as tools

pp = pprint.PrettyPrinter(indent=4)


# Configuration
folder = "E:\\Programs\\Mmed\\_Image\\Fooocus_win64_2-0-50\\Fooocus\\outputs\\test"
# folder = "E:\\Programs\\Mmed\\_Image\\Fooocus_win64_2-0-50\\Fooocus\\outputs\\2024-03-14"
file_tags = ["up2_up2_up2", "up2_up2", "up2", "up4", "orig", "thumb"]
exe = "E:\\Programs\\Mmed\\_Image\\RealEsrgan-ncnn-vulkan\\realesrgan-ncnn-vulkan.exe"


def main():
    files = get_all_files(folder)
    d = build_files_dict(files)
    clean_abandoned_json(d)
    # d = clean_up2_tags(d)
    upscale_images(d)
    # pp.pprint(d)


def upscale_images(d):
    print("SCANNING FOR IMAGES TO UPSCALE")
    for image in d:
        if "orig" in d[image]["files"]:
            if "up2" not in d[image]["files"] and "up2_up2" not in d[image]["files"]:
                upscale_image(os.path.join(folder, d[image]["files"]["orig"]))


def upscale_image(file_name):
    exe = (
        "E:\\Programs\\Mmed\\_Image\\RealEsrgan-ncnn-vulkan\\realesrgan-ncnn-vulkan.exe"
    )
    scale = 2

    if os.path.exists(file_name):

        print(f"UPSCALING: {file_name}")
        (name, ext) = os.path.splitext(os.path.basename(file_name))
        dir = os.path.dirname(file_name)

        new_file = f"{name}_up{scale}{ext}"
        new_file = os.path.join(dir, new_file)

        opt = f'-i "{file_name}" -o "{new_file}" -s {scale}'

        # subprocess.Popen(f"{exe} {opt}")
        output = subprocess.run(
            f"{exe} {opt}",
            shell=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )


def clean_up2_tags(d):
    for image in d:
        for tag in d[image]["files"]:
            if tag == "up2_up2_up2":
                d[image]["files"]["up6"] = d[image]["files"]["up2_up2_up2"]
                new_filename = f"{image}_up6.png"
                os.rename(
                    os.path.join(folder, d[image]["files"]["up2_up2_up2"]),
                    os.path.join(folder, new_filename),
                )
                d[image]["files"]["up2_up2_up2"] = ""
                d[image]["files"]["up6"] = new_filename

            if tag == "up2_up2":
                d[image]["files"]["up4"] = d[image]["files"]["up2_up2"]
                new_filename = f"{image}_up4.png"
                os.rename(
                    os.path.join(folder, d[image]["files"]["up2_up2"]),
                    os.path.join(folder, new_filename),
                )
                d[image]["files"]["up2_up2"] = ""
                d[image]["files"]["up4"] = new_filename

    return d


def clean_abandoned_json(d):
    print("SCANNING FOR ABANDONED JSON FILES")
    for image in d:
        if "json" in d[image]["files"] and len(list(d[image]["files"].keys())) == 1:
            os.remove(os.path.join(folder, d[image]["files"]["json"]))
            print(f'ABANDONED JSON FILE: {d[image]["files"]["json"]}')


def build_files_dict(files):
    print("BUILDING FILE DICTIONARY")
    d = {}

    for file_name in files:
        file_name = os.path.basename(file_name)
        (name, ext) = os.path.splitext(file_name)
        # print(name, ext)
        imgname = name
        tags = ""
        (imgname, tags) = tools.get_tags(name, file_tags)
        if ext == ".json":
            tags = "json"

        if tags == "":
            tags = "orig"

        if imgname not in d:
            d[imgname] = {}
            d[imgname]["files"] = {}

        d[imgname]["files"][tags] = file_name

    return d


def get_all_files(folder):
    print(f"GETTING FILES FROM: {folder}")
    return glob.glob(os.path.join(folder, "*.*"))


if __name__ == "__main__":
    main()
