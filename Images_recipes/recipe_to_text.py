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
import pyttsx3
engine = pyttsx3.init()




pytesseract.pytesseract.tesseract_cmd = r'C:\Users\varun\Anaconda3\Lib\site-packages\pytesseract\tesseract'
x=pytesseract.image_to_string(Image.open('rattatouille_instructions.png'))
#x=''.join(z for z in x if x.isalnum())
x=' '.join(x.split())
x=re.split('[0-9]*\.',x)
#x=(x.split(','))
print(x[5])
i=0

command=0

    
for z in x:
    number_i=str(i)
    '''
    if z=='INSTRUCTIONS':
        i=i+1
    else:
    '''
    engine.say(z)
    engine.runAndWait()
    print(i)
    #input("Press Enter to continue...")
    
    while command==0:
        
        time.sleep(.1)
        #command=hear_command()


