from tkinter import *
from PIL import Image, ImageTk


class Root(Tk):
    posX = 50
    # btn2Disabled = IntVar()
    def __init__(self):
        super().__init__()
        # self.geometry("500x500")
        self.config(bg="blue")

        self.rowconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)

        self.cnvBtn = Canvas(self, bg="green")
        self.cnvBtn.grid(row=0, column=0, sticky="es")

        self.cnv = Canvas(self, bg='orange')
        self.cnv.grid(row=1, column=1)

        # BUTTONS===============================
        self.btn1 = Button(self.cnvBtn, text="Hard move train", command=self.hardMoveImg)
        self.btn1.pack()
        self.btn2 = Button(self.cnvBtn, text="Smooth move image", command=self.smoothMoveImg)
        self.btn2.pack()
        self.btn3 = Button(self.cnvBtn, text="Change Canvas grid's position", command=self.moveCnv)
        self.btn3.pack()
        # FIN BUTTONS============================
        
        

        
        # IMAGES===============================
        self.cnvImgs = []
        self.img = Root.createImg(50, 50, "../png/wagon val.png")
        self.cnvImgs.append(self.cnv.create_image(10, 10, anchor="nw", image=self.img))
        self.cnvImgs.append(self.cnv.create_image(110, 110, anchor="nw", image=self.img))
        # FIN IMAGES============================




    def hardMoveImg(self):
        if self.posX >= 300:
            self.posX = 10


        for i in range(1, len(self.cnvImgs)):
            self.cnv.delete(self.cnvImgs[i])
            
        self.cnv.delete(self.cnvImgs[0])
        self.cnvImgs.pop(0)

        self.cnvImgs.append(self.cnv.create_image(self.posX, 60, anchor="nw", image=self.img))

        self.posX += 50

    def smoothMoveImg(self):
        if self.posX >= 300:
            self.btn2.config(state="normal")
            self.posX = 10
            return

        self.btn2.config(state="disabled")

        for i in range(1, len(self.cnvImgs)):
            self.cnv.delete(self.cnvImgs[i])
        
        self.cnv.delete(self.cnvImgs[0])
        self.cnvImgs.pop(0)

        self.cnvImgs.append(self.cnv.create_image(self.posX, 60, anchor="nw", image=self.img))

        self.posX += 5

        Tk.after(self, ms=50, func=self.smoothMoveImg)
        
    def moveCnv(self):
        print(self.grid_slaves())
        if self.grid_slaves(column=1) == []:
            self.cnv.grid(row=1, column=1)
        else:
            self.cnv.grid(row=1, column=2)



    @classmethod
    def createImg(cls, x, y, file):
        img = Image.open(file)
        img = img.resize((x, y))
        return ImageTk.PhotoImage(img)

        
root = Root()
root.mainloop()
