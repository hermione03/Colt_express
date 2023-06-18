from tkinter import *
from PIL import Image, ImageTk

icon = '../train.ico'



win = Tk()

img = Image.open(icon)
img = ImageTk.PhotoImage(img)

win.call('wm', 'iconphoto', win._w, img)

win.mainloop()
