from tkinter import *
from PIL import Image, ImageTk



class Root(Tk):
    img1 = Image.open("../png/loco_v2.png")


    def __init__(self):
        super().__init__()
        self.config(bg='orange')
        self.geometry('500x500')

        for i in range(3):
            self.rowconfigure(i, weight=1)
            self.columnconfigure(i, weight=1)


        self.btn = Button(self, bg='orange', border=0, highlightthickness=0, activebackground='brown')

        self.img = ImageTk.PhotoImage(Root.img1.resize((200, 100)))
        self.btn.config(image=self.img)

        self.btn.grid(row=1, column=1)




root = Root()
root.mainloop()
