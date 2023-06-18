from tkinter import *
import random
from PIL import Image, ImageTk


global colors
colors = {"red":(255, 0, 0, 1),
          "orange":(255, 128, 0, 1),
          "yellow":(255, 255, 0, 1),
          "green":(0, 255, 0, 1),
          "blue":(0, 0, 255, 1)}
print(type(colors["red"][3]))

global posX
global posY
posX = 0
posY = 1


class Root(Tk):
    imgs = []
    def __init__(self):
        super().__init__()
        self.config(bg="blue")
        self.geometry("600x600")

        self.rowconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)

        self.cnv = Canvas(self, width=500, height=500, bg="orange")
        self.cnv.grid(row=1, column=1)

        self.btn = Button(self, text="Change color")
        self.btn.config(command=lambda:self.drawBandit(200, 250, ["../png/bandit.png", "../png/bandit_details.png"]))
        self.btn.grid(column=1)

        






    def drawBandit(self, width, height, files):
        global posX
        global posY

        if posX == 0 and posY == 1:
            posX = 0
            posY = 0

            #on vide la canvas
            for image in self.imgs:
                self.cnv.delete(image)
            self.imgs.clear()

        elif posX == 0 and posY == 0:
            posX = 1
            posY = 0
        elif posX == 1 and posY == 0:
            posX = 1
            posY = 1
        elif posX == 1 and posY == 1:
            posX = 0
            posY = 1
        elif posX == 1 and posY == 1:
            posX = 0
            posY = 1


            
            
        color = random.choice(list(colors.values()))
        

        #=== CREATION IMG =======================
        body = Image.open(files[0])
        body = body.resize((width, height))

        #lors du resize, il y'a de l'aliasing, donc tout les pixels non completement transparent devienne noir
        # for y in range(body.height):
        #     for x in range(body.width):
        #         if body.getpixel((x, y))[3] != 0:
        #             body.putpixel((x, y), value=(0, 0, 0))

        details = Image.open(files[1])
        details = details.resize((width, height))



        #on change les pixels qui ne sont pas transparent
        for y in range(details.height):
            for x in range(details.width):
                if details.getpixel((x, y)) != (0, 0, 0, 0):
                    tempC = (color[0], color[1], color[2], details.getpixel((x, y))[3])
                    details.putpixel((x, y), value=tempC)

        self.bandit = Image.alpha_composite(body, details)
        self.bandit = ImageTk.PhotoImage(self.bandit)
        #=== FIN CREATION IMG ===================

        img = self.cnv.create_image(posX*width, posY*height, anchor="nw", image=self.bandit)
        self.imgs.append(img)

        







    @classmethod
    def createImgWithTransBg(cls, x, y, file):
        img = Image.open(file)
        img = img.resize((x, y))
        bg = Image.new('RGBA', img.size, (0, 0, 0, 0))
        newImg = Image.alpha_composite(bg, img)
        return ImageTk.PhotoImage(newImg)



root = Root()

root.mainloop()



"""
from tkinter import *

class Colors(Frame):
    def __init__(self):
        Frame.__init__(self)
        self._image = PhotoImage(file="r.gif")
        self._imageLabel = Label(self, image=self._image)
        self._imageLabel.grid()

        self.master.title("Color Changer")
        self.grid()

        self.red = Scale(self, from_=0, to=255, label="Red", fg="red", )
        self.red.grid(row=0, column=1)

        self.green = Scale(self, from_=0, to=255, label="Green", fg='green')
        self.green.grid(row=0, column=2)

        self.blue = Scale(self, from_=0, to=255, label="Blue", fg="blue")
        self.blue.grid(row=0, column=3)

        self.button = Button(self, text="Change Colors", command=self.changeColor)
        self.button.grid(row=1, column=2)

    def changeColor(self):
        red = self.red.get()
        blue = self.blue.get()
        green = self.green.get()
        for y in range(self._image.height()):
            for x in range(self._image.width()):
                self._image.put("#%02x%02x%02x" % (red,green,blue), (x, y))

def main():
    Colors().mainloop()

main()
"""