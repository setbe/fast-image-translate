from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

from PIL import Image, ImageDraw, ImageGrab, ImageQt, ImageFont
import os, os.path

cache_path = os.path.join(os.curdir, 'image_cache')
image_path = os.path.join(cache_path, 'image.png')

class Text():
    def __init__(self, string, left, top) -> None:
        self.string = string
        self.fontsize = 30
        self.color = (60, 60, 60, 255)

        self.left = left
        self.top = top

class Fit_Image():
    def __init__(self) -> None:
        self.image = None
        self.img_draw = None

        self.img_text = None
        self.text_draw = None

        self.qt_img = None
        self.texts = []
        self.selected_text = -1

        self.was_change_text = False

    def delete_text(self):
        if self.current_text():
            del self.texts[self.selected_text]
            self.selected_text = -1
            self.was_change_text = True

    def pil2pixmap(self):
        im2 = self.image.copy()
        im2 = im2.convert("RGBA")
        self.draw_text()
        im2.paste(self.img_text, mask=self.img_text)
        data = im2.tobytes("raw", "RGBA")
        self.qt_img = QImage(data, self.image.width, self.image.height, QImage.Format.Format_RGBA8888)
        return QPixmap.fromImage(self.qt_img)

    def get(self):
        self.image = Image.open(image_path)
        self.img_draw = ImageDraw.Draw(self.image)
        self.img_text = Image.new('RGBA', self.image.size, (0, 0, 0, 0))
        self.text_draw = ImageDraw.Draw(self.img_text)
        return self.update()
    
    def draw_text(self):
        self.text_draw.rectangle((0, 0, self.img_text.width, self.img_text.height), (0, 0, 0, 0))
        for i, text in enumerate(self.texts):
            font = ImageFont.truetype("calibri.ttf", text.fontsize, encoding="unic")
            if self.selected_text == i:
                wh = self.text_draw.textsize(text.string, font)
                self.text_draw.rectangle((text.left - 5, text.top - 5, text.left + wh[0] + 5, text.top + text.fontsize + 5), outline='green')
            self.text_draw.text((text.left, text.top), text.string, text.color, font)

    def update(self):
        if self.image:
            return self.pil2pixmap()
        
    def save(self):
        self.update().save("out.png")
    
    def copy(self):
        pass

    def paste(self):
        self.image = ImageGrab.grabclipboard()
        if self.image:
            self.img_draw = ImageDraw.Draw(self.image)
            self.img_text = Image.new('RGBA', self.image.size, (0, 0, 0, 0))
            self.text_draw = ImageDraw.Draw(self.img_text)
            return self.update()
        else:
            return None

    def paint(self, x: int, y: int, radius: int, color: tuple):
        self.img_draw.ellipse((x - radius / 2, y - radius / 2, x + radius / 2, y + radius / 2), color)

    def add_text(self, x: int, y: int):
        self.selected_text = len(self.texts)
        self.texts.append(Text("Some Text", x, y))
        self.was_change_text = True

    def cursor_pressed(self, x: int, y: int):
        for i, text in enumerate(self.texts):
            font = ImageFont.truetype("calibri.ttf", text.fontsize, encoding="unic")

            wh = self.text_draw.textsize(text.string, font)

            if x > text.left and x < text.left + wh[0] and y > text.top - 8 and y < text.top + wh[1] + 8:
                if self.selected_text != i:
                    self.selected_text = i
                    self.was_change_text = True

                text.left = x - wh[0] / 2
                text.top = y - wh[1] / 2
                return
        self.selected_text = -1
        self.was_change_text = True

    def current_text(self):
        if self.selected_text >= 0 and self.selected_text < len(self.texts):
            return self.texts[self.selected_text]
        return None