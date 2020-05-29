import urllib.request
import pathlib
import shutil
import os

DOWNLOADS_PATH = str(pathlib.Path().absolute()) + "/downloads"


class AudioSource:
    def __init__(self, name, url):
        self.name = name + ".wav"
        self.url = url
        self.path = ""

    def download(self):
        folder = f"{DOWNLOADS_PATH}/temp/"
        filepath = folder + self.name
        urllib.request.urlretrieve(f"{self.url}.wav", filepath)
        self.path = filepath

    def delete_file(self):
        os.remove(self.path)

    def move(self, to="/faileds/"):
        shutil.move(self.path, f"{DOWNLOADS_PATH}{to}{self.name}")
        self.path = f"{DOWNLOADS_PATH}{to}{self.name}"
