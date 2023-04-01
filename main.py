from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

from googletrans import Translator, constants
from enum import Enum

from window import Ui_MainWindow
from image import Fit_Image, image_path
from text_extractor import *

import cv2
import numpy as np

class Tool(Enum):
    CURSOR = 1
    BRUSH = 2
    TEXT = 3

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.setupUi(self)
        self.image = Fit_Image()
        self.tool = Tool.BRUSH

        self.setWindowIcon(QIcon('fit.png'))
        self.shortcut_paste = QShortcut(QKeySequence("Ctrl+V"), self)
        self.shortcut_paste.activated.connect(self.paste)
        self.shortcut_copy = QShortcut(QKeySequence("Ctrl+C"), self)
        self.shortcut_copy.activated.connect(self.copy)

        self.langs = []
        for name in constants.LANGUAGES.values():
            self.langs.append(name)

        self.lang_from.addItems(self.langs)
        self.lang_to.addItems(self.langs)

        self.btn_reverse.pressed.connect(self.reverse_languages)
        self.lang_from.setCurrentText('russian')
        self.lang_to.setCurrentText('ukrainian')

    def reverse_languages(self):
        temp = self.lang_from.currentText()
        self.lang_from.setCurrentText(self.lang_to.currentText())
        self.lang_to.setCurrentText(temp)

    def copy(self):
        self.image.copy()

    def paste(self):
        self.label.setPixmap(self.image.get())
        #self.label.setPixmap(self.image.paste())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            last_point = event.pos()
            print(last_point)
            
    def mouseMoveEvent(self, event):
        if (event.buttons() == Qt.LeftButton):
            pass

    def maintain_ratio(image, width=None, height=None, inter=cv2.INTER_AREA):
        dim = None
        (h, w) = image.shape[:2]

        if width is None and height is None:
            return image
        
        if width is None:
            r = height / float(h)
            dim = (int(w * r), height)
        else:
            r = width / float(w)
            dim = (width, int(h * r))
        return cv2.resize(image, dim, interpolation=inter)
    


import sys


get_text('eng')
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     win = MainWindow()

#     # temp = cv2.imread(image_path)
#     # temp = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
#     # temp = cv2.Canny(temp, 50, 200)
#     # (tH, tW) = temp.shape[:2]
#     # cv2.imshow('temp', temp)
#     win.show()
#     sys.exit(app.exec_())