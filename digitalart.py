import os
import utlis.jbf.file as file
import utlis.jbf.tools as tools
import utlis.jbf.toml as toml
import pprint

pp = pprint.PrettyPrinter(indent=4)


class Session:
    def __init__(self, folder: str, config: dict):
        self.folder = folder
        self.timestart = ""
        self.timeend = ""
        self.images = {}
        self.config = config
        self.files = []

        self.scan()

    def __str__(self):
        # return f"Session: folder={self.folder}"
        return pp.pformat(self)

    def __repr__(self):
        return pp.pformat(self)

    def scan(self):
        self.files = file.scandir(self.folder)
        for f in self.files:
            (name, tag) = tools.get_tags(f, self.config['app']['file_tags'])
            if name not in self.images:
                self.addimage(name)

    def addimage(self, imagename):
        self.images[imagename] = Image(imagename, self.config, self.folder)



class Image:
    def __init__(self, imagename, config, folder):
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
        files = file.scandir(self.folder, f"{self.imagename}*")

        for f in files:
            (name, tag) = tools.get_tags(
                f,
                self.config["app"]["file_tags"],
                self.config["app"]["image_file_extensions"],
            )

            if tag not in self.files:
                self.files[tag] = f

    def toml_load_file(self):
        if 'toml' in self.files['toml']:
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
        pass

    def get_ai_description(self):
        pass
