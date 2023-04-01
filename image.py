from PIL import Image, ImageDraw, ImageGrab
import os, os.path

current_path = os.curdir
cache_path = os.path.join(current_path, 'image_cache')
image_path = os.path.join(cache_path, 'image.png')

class Fit_Image():
    def __init__(self) -> None:
        self.image = None
        
    def copy(self):
        print("copied")

    def paste(self):
        self.image = ImageGrab.grabclipboard()
        if self.image:
            pass
        self.replace_image_cache()

    def replace_image_cache(self):
        if not os.path.exists(cache_path):
            os.mkdir(cache_path)
        self.image.save(image_path)

    def image_exists(self):
        if os.path.isfile(image_path):
            return True
        return False


