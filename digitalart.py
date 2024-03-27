import os
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
        patterns.append('.toml')
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
        for img in self.images:
            self.images[img].get_ai_description()



class Image:
    def __init__(self, imagename, config, folder):
        log.debug(f"new image: name={imagename}")
        self.imagename = imagename
        self.source = ""
        self.fooocus = {}
        self.files = {}
        self.ai = {}
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
        if 'toml' in self.files:
            log.debug(f"loading toml file: name={self.imagename}")
            t = toml.load_file(os.path.join(self.folder, self.files['toml']))
            self.toml_str = toml.to_toml(t)

            if 'fooocus' in t:
                self.fooocus = t['fooocus']

            if 'ai' in t:
                self.ai = t['ai']

    def toml_build_str(self):
        t = {}
        t['files'] = self.files
        t['fooocus'] = self.fooocus
        t['ai'] = self.ai
        t["source"] = self.source
        t['imagename'] = self.imagename
        t["status"] = self.status
        self.toml_str = toml.to_toml(t)

    def toml_write_file(self):
        self.toml_build_str()
        t = toml.toml_parse(self.toml_str)
        toml.save_file(os.path.join(self.folder, f"{self.imagename}.toml"), t)
        self.files["toml"] = f"{self.imagename}.toml"

    def get_fooocus(self):
        log_file = os.path.join(self.folder, 'log.html')
        if os.path.exists(log_file) and not self.fooocus:
            log_html = file.read_file(log_file)
            log.debug(f"{self.imagename} : get fooocus")
            self.fooocus = bs.metadata_from_log(log_html, f"{self.imagename}.png")
            self.toml_write_file()
            

    def get_ai_description(self):
        if not self.ai:
            img_file = ''
            if 'thumb' in self.files:
                img_file = self.files['thumb']
            elif 'orig' in self.files:
                img_file = self.files['orig']

            if img_file != "":
                prompt = "no extra information available"
                if self.fooocus:
                    prompt = self.fooocus['Prompt']

                img_file = os.path.join(self.folder, img_file)

                self.ai = api.analyze_image(
                    img_file,
                    self.config["ai"]["system_msg_file"],
                    prompt,
                    self.config["ai"]["model"],
                )

                self.toml_write_file()
