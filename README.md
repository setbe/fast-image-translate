# FIT (Fast Image Translate)

Desktop application for translating text inside images using OCR, automatic translation, and manual visual editing.

Built for real-world productivity: documents, screenshots, scans, medical materials, educational content, and any image that contains foreign-language text.

---

# Overview

Many OCR tools only extract text.
Many translators ignore layout.
Many image editors are too slow for quick translation work.

FIT combines all three workflows in one desktop tool:

- detect text from image
- translate automatically
- remove original text manually where needed
- place translated text exactly in the original layout
- export final translated image

---

# Real Origin Story

This project was created after a doctor needed fast Ukrainian translation of medical image materials.

The first working version was designed and built from scratch in 48 hours using Python, PyQt, OCR, and translation APIs.

---

# Key Features

- Clipboard image paste (Ctrl + V)
- OCR text detection
- Automatic translation
- Manual brush cleanup
- Move translated text precisely
- Text size and color controls
- Save final result

---

# Screenshots

![Preview 1](https://user-images.githubusercontent.com/70776479/229385339-9cbf22a0-a31c-461d-8a4c-855dab5a850f.png)

![Preview 2](https://user-images.githubusercontent.com/70776479/229385367-a32b6111-ab62-4533-9a19-adf61885bb6e.png)

![Preview 3](https://user-images.githubusercontent.com/70776479/229385221-4d6465f2-e2c2-4543-8c26-e734f5ccac71.png)

---

# Technologies Used

- Python
- PyQt5
- Tesseract OCR
- OpenCV
- Pillow
- Google Translate API

---

# Run

```bash
pip install -r requirements.txt
python main.py
```

---

# Author

Developed by **setbe**.

---

# License

MIT License
