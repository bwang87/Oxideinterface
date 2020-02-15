# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 22:39:59 2020

@author: varun
"""
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\varun\Anaconda3\Lib\site-packages\pytesseract\tesseract'
x=pytesseract.image_to_string(Image.open('rattatouille_instructions.png'))
#x=''.join(z for z in x if x.isalnum())
x=' '.join(x.split())
x=(x.split(','))
print(x)
