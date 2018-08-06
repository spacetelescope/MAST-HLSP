from bin.read_yaml import read_yaml
from FileType import FileType
from FitsKeyword import FitsKeyword
import re
import yaml

try:
    from PyQt5.QtCore import pyqtSignal
except ImportError:
    from PyQt4.QtCore import pyqtSignal


class HLSPFile(object):

    def __init__(self, path=None):
        super().__init__()

        steps = ["filenames_checked", "metadata_checked", "files_selected"]
        self._prep_level = 0
        self._updated = False

        self.file_paths = {"InputDir": "", "Output": ""}
        self.file_types = []
        self.hlsp_name = "Blank"
        self.ingest = {s: False for s in steps}
        self.keyword_updates = []
        self.unique_parameters = {}

        if path:
            self.load_hlsp(path)

    def add_filetype(self, ftype):

        self.file_types.append(ftype.as_dict())

    def add_keyword_update(self, keyword):

        if isinstance(keyword, FitsKeyword):
            self.keyword_updates.append(keyword)
        else:
            raise TypeError("Only FitsKeyword objects should be added.")

    def as_dict(self):

        file_formatted_dict = {}
        for key, val in self.__dict__.items():
            if key[0] == "_":
                continue
            key = key.split("_")
            key = "".join([k.capitalize() for k in key])
            file_formatted_dict[key] = val

        return file_formatted_dict

    def load_hlsp(self, filename):

        load_dict = read_yaml(filename)
        for key, val in load_dict.items():
            key = re.findall('[A-Z][^A-Z]*', key)
            attr = "_".join([k.lower() for k in key])
            setattr(self, attr, val)

    def save(self, filename=None):

        if filename:
            if not filename.endswith(".hlsp"):
                filename = ".".join([filename, "hlsp"])
        else:
            filename = ".".join([self.hlsp_name, "hlsp"])

        with open(filename, 'w') as yamlfile:
            yaml.dump(self.as_dict(), yamlfile, default_flow_style=False)

    def toggle_updated(self, flag):
        self.updated = flag

    def update_filepaths(self, input=None, output=None):

        new_paths = {}

        if input:
            new_paths["InputDir"] = input
        if output:
            new_paths["Output"] = output

        self.file_paths.update(new_paths)


def __test__():
    h = HLSPFile()
    h.save("test_ouput")


if __name__ == "__main__":
    __test__()
