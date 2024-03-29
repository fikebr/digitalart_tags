import os
import csv
import time
import utlis.jbf.file as file
import utlis.jbf.tools as tools
import utlis.jbf.toml as toml
import utlis.jbf.bsoup as bs
import utlis.jbf.claude as api
import pprint
import logging

pp = pprint.PrettyPrinter(indent=4)
log = logging.getLogger(__name__)


class Session:
    def __init__(self, folder: str, config: dict):
        self.folder = folder
        self.timestart = ""
        self.timeend = ""
        self.images = {}
        self.config = config
        self.files = []

        self.scan()

    def scan(self):
        patterns = []
        patterns = self.config["app"]["image_file_extensions"]
        patterns.append(".toml")
        patterns = list(map(lambda x: f"*{x}", patterns))

        self.files = file.scandir(self.folder, patterns)
        for f in self.files:
            (name, tag) = tools.get_tags(
                f,
                self.config["app"]["file_tags"],
                self.config["app"]["image_file_extensions"],
            )
            if name not in self.images:
                self.addimage(name)

    def addimage(self, imagename):
        self.images[imagename] = Image(imagename, self.config, self.folder)

    def get_fooocus(self):
        for img in self.images:
            self.images[img].get_fooocus()

    def get_ai_description(self):

        if self.config['ai']['api_pause'] > 0:
            time.sleep(self.config["ai"]["api_pause"])

        for img in self.images:
            self.images[img].get_ai_description()

    def upscale(self):
        log.info("Scanning for images to upscale.")
        for img in self.images:
            self.images[img].upscale()

    def toml_write(self):
        for img in self.images:
            self.images[img].toml_write_file()

    def toml_clean_abandoned(self):
        log.info("Scanning for abandoned toml files.")
        for img in self.images:
            self.images[img].toml_clean_abandoned()
            

    def adobe_stock_csv(self):
        rows = []
        head = ["Filename", "Title", "Keywords", "Category", "Releases"]
        rows.append(head)

        for img in self.images:
            row = self.images[img].adobe_stock_row()

            if row:
                rows.append(row)

        csv_filename = os.path.join(self.folder, "adobe_stock.csv")

        with open(csv_filename, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)

            # Write each row of data to the CSV file
            for r in rows:
                writer.writerow(r)
    
    def adobe_stock_mark_posted(self):
        for img in self.images:
            self.images[img].mark_posted_to('adobe_stock')


class Image:
    def __init__(self, imagename, config, folder):
        log.debug(f"new image: name={imagename}")
        self.imagename = imagename
        self.source = ""
        self.fooocus = {}
        self.files = {}
        self.ai = {}
        self.biz = {}
        self.status = "new"
        self.toml_str = ""
        self.folder = folder
        self.config = config

        self.get_files()
        self.toml_load_file()

    def __str__(self):
        return f"Image: {self.imagename} ({self.status})"

    def get_files(self):
        image_files = []
        pattern = [f"{self.imagename}*.*"]
        image_files = file.scandir(self.folder, pattern)

        for f in image_files:
            (name, tag) = tools.get_tags(
                f,
                self.config["app"]["file_tags"],
                self.config["app"]["image_file_extensions"],
            )

            if tag != "" and tag not in self.files:
                self.files[tag] = f

    def toml_load_file(self):
        if "toml" in self.files:
            log.debug(f"loading toml file: name={self.imagename}")
            t = toml.load_file(os.path.join(self.folder, self.files["toml"]))
            self.toml_str = toml.to_toml(t)

            if "fooocus" in t:
                self.fooocus = t["fooocus"]

            if "ai" in t:
                self.ai = t["ai"]

            if "biz" in t:
                self.biz = t["biz"]

    def toml_build_str(self):
        t = {}
        t["files"] = self.files
        t["fooocus"] = self.fooocus
        t["ai"] = self.ai
        t["biz"] = self.biz
        t["source"] = self.source
        t["imagename"] = self.imagename
        t["status"] = self.status
        self.toml_str = toml.to_toml(t)

    def toml_write_file(self):
        self.toml_build_str()
        t = toml.toml_parse(self.toml_str)
        toml.save_file(os.path.join(self.folder, f"{self.imagename}.toml"), t)
        self.files["toml"] = f"{self.imagename}.toml"

    def toml_clean_abandoned(self):
        file_count = len(self.files.keys())
        is_toml = False
        if 'toml' in self.files:
            is_toml = True

        if file_count == 1 and is_toml:
            log.info(f"deleting toml file: {self.files['toml']}")
            os.remove(os.path.join(self.folder, self.files['toml']))
            del self.files['toml']
            

    def mark_posted_to(self, service):
        if 'posted_to' not in self.biz:
            self.biz['posted_to'] = []
        
        self.biz["posted_to"].append(service)
        self.toml_write_file()

    def get_fooocus(self):
        log_file = os.path.join(self.folder, "log.html")
        if os.path.exists(log_file) and not self.fooocus:
            self.source = 'fooocus'
            log_html = file.read_file(log_file)
            log.debug(f"{self.imagename} : get fooocus")
            self.fooocus = bs.metadata_from_log(log_html, f"{self.imagename}.png")
            self.toml_write_file()

    def get_ai_description(self):
        if not self.ai:
            img_file = ""
            if "thumb" in self.files:
                img_file = self.files["thumb"]
            elif "orig" in self.files:
                img_file = self.files["orig"]

            if img_file != "":
                prompt = "no extra information available"
                if self.fooocus:
                    prompt = self.fooocus["Prompt"]

                img_file = os.path.join(self.folder, img_file)

                response = api.analyze_image(
                    img_file,
                    self.config["ai"]["system_msg_file"],
                    prompt,
                    self.config["ai"]["model"],
                )

                if response:
                    self.ai = response
                    self.toml_write_file()

    def upscale(self):
        scale = self.config["upscale"]["scale"]
        tag = f"up{scale}"

        if tag not in self.files and "orig" in self.files:
            log.info(f"{self.imagename} needs upscale.")
            exe = self.config["upscale"]["exe"]

            image_file = os.path.join(self.folder, self.files["orig"])
            (name, ext) = os.path.splitext(self.files["orig"])
            new_file = f"{name}_up{scale}{ext}"
            log.info(f"Creating new file {new_file}.")
            new_file = os.path.join(self.folder, new_file)

            opt = f'-i "{image_file}" -o "{new_file}" -s {scale}'

            output = tools.execute(f"{exe} {opt}")
            self.get_files()
            self.toml_write_file()

    def ai_keywords_to_biz_tags(self):
        if "tags" not in self.biz:
            self.biz["tags"] = ""

        if "keywords" in self.ai and self.biz["tags"] == "":
            keywords = self.ai["keywords"]  # ar
            colors = self.ai["colors"]  # ar
            art_style = self.ai["art_style"]  # str
            location = self.ai["location"]  # str
            holiday = self.ai["holiday"]  # str

            keywords = keywords + colors
            keywords = keywords + art_style.split(", ")
            keywords = keywords + location.split(", ")
            keywords = keywords + holiday.split(", ")

            self.biz["tags"] = ", ".join(keywords)

            self.toml_write_file

    def adobe_stock_row(self):

        already_on_adobe = False
        if 'posted_to' in self.biz:
            if 'adobe_stock' in self.biz['posted_to']:
                already_on_adobe = True
        
        if "title" in self.ai and not already_on_adobe:
            self.ai_keywords_to_biz_tags()

            # Filename, Title, Keywords, Category, Releases
            title = self.ai["title"]
            desc = self.ai["description"]
            keywords = self.biz["tags"]
            category = ""
            filename = ""

            if "up4" in self.files:
                filename = self.files["up4"]
            elif "up2" in self.files:
                filename = self.files["up2"]

            if filename != "":
                title = title + " | " + desc
                title = title[:195]
                return [filename, title, keywords, category, ""]

        return ""
