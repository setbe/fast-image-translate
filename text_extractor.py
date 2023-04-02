import pytesseract, cv2
import numpy as np

from pytesseract import Output
from enum import Enum
from image import image_path, Text

from io import StringIO

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

def increase_brightness(img, value=30):
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    h, s, v = cv2.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2RGB)
    return img

def get_text(language) -> Text:
    img = cv2.imread(image_path)
    
    img = increase_brightness(img)
    d = pytesseract.image_to_string(img, lang=language, config='--psm 11')
    #print(d)
    d = pytesseract.image_to_data(img, output_type=Output.DICT, lang=language, config='--psm 11')
    n_boxes = len(d['level'])
    strings = ''
    positions = []


    for i in range(n_boxes):
        if i == 0:
            continue
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        #cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        strings += d['text'][i]
        strings += '\n'

        positions.append([x, y])

    texts = []
    s = ''
    line_pos = []
    line_started = False
    saved = True

    strIO = StringIO(strings)
    for i, line in enumerate(strIO):
        if line != '\n':
            s += line.strip() + ' '
            if not line_started:
                line_pos = positions[i]
                line_started = True
            saved = False
        else:
            if not saved:
                texts.append(Text(s, line_pos[0], line_pos[1]))
                saved = True
                s = ''
                line_pos = []
                line_started = False
    if not saved:
        texts.append(Text(s, line_pos[0], line_pos[1]))
    
    return texts