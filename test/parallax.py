from tkinter import *
from PIL import Image, ImageTk

# from goto import with_goto

global time
time = 0

global repoPath
repoPath = '../png/work_in_progress/'



class Root(Tk):
    imgs = []
    images = []

    def __init__(self):


        super().__init__()
        self.geometry("900x650")

        self.config(bg="blue")

        self.rowconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)

        self.btn = Button(self, text="Start")
        self.btn.config(command=self.parallax)
        self.btn.grid(column=1)


        
        self.cnv = Canvas(self, width=800, height=600, bg="orange")
        self.cnv.grid(row=1, column=1)


        for _ in range(5):
            Root.images.append(Image())

        




    @staticmethod
    def createLoadedImd(witdh, height, img):
        img = img.resize((witdh, height))
        return ImageTk.PhotoImage(img)



    def parallax(self):
        global time
        for img in Root.imgs:
            self.cnv.delete(img)
        Root.imgs.clear()

        if time == 2000:
            time = 0

        widthCanvas = self.cnv.winfo_width()
        heightCanvas = self.cnv.winfo_height()


        nb = 0

        #1 back
        self.images[nb] = Root.createLoadedImd(widthCanvas, heightCanvas, Image.img1)
        img = self.cnv.create_image(0, 0, anchor="nw", image=self.images[nb])
        Root.imgs.append(img)

        nb += 1

        #2 mountain
        self.images[nb] = Root.createLoadedImd(widthCanvas, heightCanvas, Image.img2)
        img = self.cnv.create_image(0, 0, anchor="nw", image=self.images[nb])
        Root.imgs.append(img)

        nb += 1

        #3 rails
        self.images[nb] = Root.createLoadedImd(widthCanvas, heightCanvas, Image.img3)
        img = self.cnv.create_image(0, 0, anchor="nw", image=self.images[nb])
        Root.imgs.append(img)

        nb += 1

        #4 rock
        self.images[nb] = Root.createLoadedImd(widthCanvas, heightCanvas, Image.img4)
        img = self.cnv.create_image(0, 0, anchor="nw", image=self.images[nb])
        Root.imgs.append(img)

        nb += 1


        #loco
        self.images[nb] = Root.createLoadedImd((widthCanvas//4)*2, heightCanvas//3, Image.imgLoco)
        img = self.cnv.create_image(widthCanvas//3, heightCanvas//3, anchor="nw", image=self.images[nb])
        Root.imgs.append(img)




        time += 1
        if time%1000 == 0 :
            print("================")

        print(time)
        

        self.after(ms=1000, func=self.parallax)

        




class Image:
    imgLoco = Image.open("../png/loco val v2.png")

    img1 = Image.open(repoPath + '1_back.png')
    img2 = Image.open(repoPath + '2_mountain.png')
    img3 = Image.open(repoPath + '3_rails.png')
    img4 = Image.open(repoPath + '4_rock.png')

    def __init__(self):
        self.img = None






root = Root()


root.mainloop()

