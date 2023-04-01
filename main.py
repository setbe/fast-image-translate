from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from googletrans import Translator, constants

from window import Ui_MainWindow
from image import Fit_Image, image_path

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.setupUi(self)
        self.image = Fit_Image()

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
        self.image.paste()
        if self.image.image_exists():
            qt_img = QImage(image_path)
            pixmap = QPixmap.fromImage(qt_img)
            pixmap_img = QPixmap(pixmap)
            self.label.setPixmap(pixmap_img)


import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())