from tkinter import *

global MAX_ACTIONS
MAX_ACTIONS = 7


class Root(Tk):
    actions = []

    def __init__(self):
        super().__init__()

        self.config(bg='blue')
        self.geometry('800x500')
        
        for i in range(3):
            self.columnconfigure(i, weight=1)
        for i in range(4):
            self.rowconfigure(i, weight=1)



        self.frm = Frame(self, bg='orange', width=150, height=150)
        self.frm.grid(row=1, column=1, ipadx=10, ipady=10)

        for i in range(7):
            if i == 3 | 5:
                self.frm.rowconfigure(i, weight=2)
            else:
                self.frm.rowconfigure(i, weight=1)
        
        for i in range(5):
            self.frm.columnconfigure(i, weight=1)


        self.btn1 = Button(self.frm, text='A', command=lambda:self.addAction('A'))
        self.btn2 = Button(self.frm, text='B', command=lambda:self.addAction('B'))
        self.btn3 = Button(self.frm, text='C', command=lambda:self.addAction('C'))
        self.btn4 = Button(self.frm, text='D', command=lambda:self.addAction('D'))
        self.btn5 = Button(self.frm, text='E', command=lambda:self.addAction('E'))
        self.lab = Label(self.frm, text=f'Actions (Max:{MAX_ACTIONS})')
        self.valid = Button(self.frm, text='Valider', state='disabled', command=self.validActions)


        self.btn1.grid(row=1, column=0)
        self.btn2.grid(row=1, column=1)
        self.btn3.grid(row=1, column=2)
        self.btn4.grid(row=1, column=3)
        self.btn5.grid(row=1, column=4)
        self.lab.grid(row=3, column=0, columnspan=5)
        self.valid.grid(row=6, column=0, columnspan=5)



        self.actionsFrame = Frame(self.frm, bg='red')
        self.actionsFrame.rowconfigure(0, weight=1)
        for i in range(MAX_ACTIONS):
            self.actionsFrame.columnconfigure(i, weight=1)

        self.actionsFrame.grid(row=5, column=0, columnspan=5)


        self.complete = Label(self, bg='green')
        self.complete.grid(row=3, column=1)






    def addAction(self, value):
        if len(Root.actions) >= MAX_ACTIONS:
            print("Action bar is full")
            return

        newAction = Action(self, self.actionsFrame, value, len(self.actions))
        self.actions.append(newAction)
        self.updateActionsBar()



    def removeAction(self, actionToRemove):
        founded = False
        for action in self.actions:
            if founded:
                action.column -= 1
                continue
            if action == actionToRemove:
                founded = True
        
        if not founded:
            print("error: action not removed")
            return

        self.actions.remove(actionToRemove)
        self.updateActionsBar()



    def updateActionsBar(self):
        #clear actions bar
        for widget in self.actionsFrame.grid_slaves(row=0):
            widget.grid_remove()
        
        #fill it
        for action in Root.actions:
            action.grid(row=0, column=action.column)

        #update "valider" button state
        if len(self.actions) == MAX_ACTIONS:
            self.valid.config(state='normal')
        else:
            self.valid.config(state='disabled')



    def clearActionsBar(self):
        for widget in self.actionsFrame.grid_slaves(row=0):
            widget.grid_remove()
        
        self.actions.clear()
        self.updateActionsBar()



    def validActions(self):
        self.complete["text"] += '\n'
        for action in self.actions:
            self.complete["text"] += action.value + ' '
        
        self.clearActionsBar()
    











class Action(Frame):
    def __init__(self, root:Tk, actionsFrame:Frame, value:str, column:int):
        super().__init__(actionsFrame, bg='orange')
        self.root:Tk = root
        self.column:int = column
        self.value:str = value

        self.action = Button(self, text=value, command=self.remove)
        self.left = Button(self, text="<-", command=self.moveLeft)
        self.right = Button(self, text="->", command=self.moveRight)

        self.action.grid(columnspan=2)
        self.left.grid(row=1)
        self.right.grid(row=1, column=1)



    def __str__(self):
        return (f'{self.value}:{self.column}')



    def remove(self):
        for action in self.root.actions:
            if action == self:
                self.after(ms=1, func=lambda:self.root.removeAction(self))
                return



    def moveRight(self):
        if (self.column >= MAX_ACTIONS-1) or (self.column >= len(self.root.actions)-1):
            print("Can't move right")
            return


        for i, action in enumerate(self.root.actions):
            if action == self:
                actionTo = self.root.actions[i+1]

                #swap values
                self.value, actionTo.value = actionTo.value, self.value

                #update Action(s)
                self.update()
                actionTo.update()



    def moveLeft(self):
        if self.column <= 0:
            print("Can't move left")
            return


        for i, action in enumerate(self.root.actions):
            if action == self:
                actionTo = self.root.actions[i-1]

                 #swap values
                self.value, actionTo.value = actionTo.value, self.value

                #update Action(s)
                self.update()
                actionTo.update()



    def update(self):
        self.action.config(text=self.value)
        
        








root = Root()

root.mainloop()