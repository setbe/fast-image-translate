from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QEvent

from googletrans import Translator, constants, LANGUAGES
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
        self.tool = Tool.CURSOR

        self.c_brush = QColorDialog()
        self.c_brush.setCurrentColor(Qt.white)
        self.c_text = QColorDialog()
        self.c_text.setCurrentColor(Qt.black)
        self.c_text.currentColorChanged.connect(self.text_color_changed)


        self.setWindowIcon(QIcon('fit.png'))
        self.shortcut_paste = QShortcut(QKeySequence("Ctrl+V"), self)
        self.shortcut_paste.activated.connect(self.paste)
        self.shortcut_copy = QShortcut(QKeySequence("Ctrl+C"), self)
        self.shortcut_copy.activated.connect(self.copy)
        self.shortcut_copy = QShortcut(QKeySequence("Ctrl+S"), self)
        self.shortcut_copy.activated.connect(self.save)

        self.shortcut_delete = QShortcut(QKeySequence("Delete"), self)
        self.shortcut_delete.activated.connect(self.delete_text)

        self.langs = []
        for name in constants.LANGUAGES.values():
            self.langs.append(name)

        self.lang_from.addItems(self.langs)
        self.lang_to.addItems(self.langs)

        self.btn_reverse.pressed.connect(self.reverse_languages)
        self.brush_color.pressed.connect(self.get_color_brush)
        self.text_color.pressed.connect(self.get_color_text)

        self.btn_cursor.pressed.connect(self.set_cursor_tool)
        self.btn_brush.pressed.connect(self.set_brush_tool)
        self.btn_text.pressed.connect(self.set_text_tool)

        self.text_size.valueChanged.connect(self.text_size_changed)
        self.line_edit.textChanged[str].connect(self.filter_callback)

        self.lang_from.setCurrentText('russian')
        self.lang_to.setCurrentText('ukrainian')

    def delete_text(self):
        self.image.delete_text()
        self.label.setPixmap(self.image.update())

    def check_selected_text_update(self):
        if self.image.was_change_text and self.image.current_text():
            text = self.image.texts[self.image.selected_text]

            self.line_edit.setText(text.string)

            self.c_text.setCurrentColor(QColor(text.color[0], text.color[1], text.color[2], text.color[3]))

            self.text_size.setValue(text.fontsize)

            self.image.was_change_text = False

    def translate(self):
        land_code = list(LANGUAGES.keys())[list(LANGUAGES.values()).index(self.lang_to.currentText())]
        translator = Translator()
        for text in self.image.texts:
            text.string = translator.translate(text.string, 'uk').text

    def text_color_changed(self):
        if self.image.current_text():
            text = self.image.texts[self.image.selected_text]
            rgba = self.c_text.currentColor().getRgb()
            text.color = rgba
            self.label.setPixmap(self.image.update())

    def text_size_changed(self):
        if self.image.current_text():
            self.image.texts[self.image.selected_text].fontsize = self.text_size.value()
            self.label.setPixmap(self.image.update())

    def filter_callback(self):
        if self.image.current_text():
            self.image.texts[self.image.selected_text].string = self.line_edit.text()
            self.label.setPixmap(self.image.update())

    def set_cursor_tool(self):
        self.tool = Tool.CURSOR
        self.label_tool.setText('Selected: Cursor')

    def set_brush_tool(self):
        self.tool = Tool.BRUSH
        self.label_tool.setText('Selected: Brush')
        
    def set_text_tool(self):
        self.tool = Tool.TEXT
        self.label_tool.setText('Selected: Text')

    def reverse_languages(self):
        temp = self.lang_from.currentText()
        self.lang_from.setCurrentText(self.lang_to.currentText())
        self.lang_to.setCurrentText(temp)

    def copy(self):
        self.image.copy()

    def save(self):
        self.image.save()

    def paste(self):
        #self.label.setPixmap(self.image.get())
        px = self.image.paste()
        if px:
            self.label.setPixmap(px)
            new_texts = get_text('rus+eng')
            for text in new_texts:
                self.image.texts.append(text)
            self.translate()
            self.image.was_change_text = True
            self.check_selected_text_update()
            self.label.setPixmap(self.image.update())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            last_point = event.pos()
            last_point.setX(last_point.x() - self.label.x())
            last_point.setY(last_point.y() + 9*3 - (self.geometry().height() - self.label.height()))

            w, h = self.label.width(), self.label.height()
            ww, hh = self.image.image.width, self.image.image.height

            last_point.setX(last_point.x() - (w - ww) / 2 - 9)
            last_point.setY(last_point.y() - (h - hh) / 2 + 23)

            if last_point.x() >= 0 and last_point.y() >= 0 and last_point.x() < ww and last_point.y() < hh:
                if self.tool == Tool.TEXT:
                    self.image.add_text(last_point.x(), last_point.y())
                    self.check_selected_text_update()
                    self.label.setPixmap(self.image.update())
            
    def mouseMoveEvent(self, event):
        if (event.buttons() == Qt.LeftButton):
            last_point = event.pos()
            last_point.setX(last_point.x() - self.label.x())
            last_point.setY(last_point.y() + 9*3 - (self.geometry().height() - self.label.height()))

            w, h = self.label.width(), self.label.height()
            ww, hh = self.image.image.width, self.image.image.height

            last_point.setX(last_point.x() - (w - ww) / 2 - 9)
            last_point.setY(last_point.y() - (h - hh) / 2 + 23)

            if last_point.x() >= 0 and last_point.y() >= 0 and last_point.x() < ww and last_point.y() < hh:

                if self.tool == Tool.BRUSH:
                    rgba = self.c_brush.currentColor().getRgb()
                    self.image.paint(last_point.x(), last_point.y(), self.brush_size.value(), rgba)
                    self.label.setPixmap(self.image.update())

                elif self.tool == Tool.CURSOR:
                    self.image.cursor_pressed(last_point.x(), last_point.y())
                    self.check_selected_text_update()
                    self.label.setPixmap(self.image.update())

                

    def get_color_brush(self):
        self.c_brush.setCurrentColor(self.c_brush.getColor())
    
    def get_color_text(self):
        self.c_text.setCurrentColor(self.c_text.getColor())
    


import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())