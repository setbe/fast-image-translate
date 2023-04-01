import pytesseract, cv2
from pytesseract import Output
from enum import Enum
from image import image_path

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

class Text():
    def __init__(self) -> None:
        self.string = ''
        self.bold = False
        self.fontsize = 0

        self.left = 0
        self.top = 0
        self.width = 0
        self.height = 0

def get_text(language) -> Text:
    img = cv2.imread(image_path)
    d = pytesseract.image_to_data(img, output_type=Output.DICT, lang=language)
    n_boxes = len(d['level'])
    
    for i in range(n_boxes):
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    cv2.imshow('img', img)
    cv2.waitKey(0)

#print(pytesseract.image_to_string('img/1.bmp', lang='rus'))