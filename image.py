from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

from PIL import Image, ImageDraw, ImageGrab
import os, os.path

cache_path = os.path.join(os.curdir, 'image_cache')
image_path = os.path.join(cache_path, 'image.png')

class Fit_Image():
    def __init__(self) -> None:
        self.image = None
        self.qt_img = None
        self.qt_img = QImage(image_path)

    def get(self):
        return QPixmap.fromImage(self.qt_img)

        
    def copy(self):
        print("copied")

    def paste(self):
        self.image = ImageGrab.grabclipboard()
        if self.image:
            self.replace_image_cache()
            if self.image_exists():
                self.qt_img = QImage(image_path)
                return QPixmap.fromImage(self.qt_img)

    def replace_image_cache(self):
        if not os.path.exists(cache_path):
            os.mkdir(cache_path)
        self.image.save(image_path)

    def image_exists(self):
        if os.path.isfile(image_path):
            return True
        return False


