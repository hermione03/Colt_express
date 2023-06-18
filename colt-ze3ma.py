import random
from tkinter import *
from typing import Literal
import modules.saveGestion as saveGestion
import modules.images as images
import modules.menus as menus
import modules.widgets as widgets
import modules.tools as tools
import modules.audios as audios

from modules.wagon import Wagon
from modules.bandit import Bandit
from modules.butin import Butin





class Game(Tk):
    #globales
    NB_JOUEURS = 4
    NB_WAGONS = 4
    NB_TOURS = 3
    MAX_ACTIONS = int(NB_JOUEURS * 1.5)
    MAX_BULLETS = NB_JOUEURS * 3
    MIN_BUTINS = 1
    MAX_BUTINS = 4

    LOAD_SAVE = FALSE

    COLORS:dict[tuple[int]] = {
        'Red':    (238, 4, 16),
        'Green':  (15, 151, 3),
        'Blue':   (10, 45, 221),
        'Pink':   (252, 133, 239),
        'Purple':   (99, 7, 87),
        'Yellow':   (233, 255, 9)}

    WIDGET_COLORS:dict[str] = {
        'red':           '#b13001',
        'redLight':      '#ca3904',
        'sand':          '#c1880b',
        'train':         '#723f02',
        'road':          '#e5b13f',
        'moutainShadow': '#976700'}

    VOLUME_GLOBAL = 75
    VOLUME_MUSIC = 25
    VOLUME_SOUNDS = VOLUME_GLOBAL



    wagons:Wagon = []
    bandits:Bandit = []
    butins:Bandit = []

    #lists used during preparation phase
    tempName:str = ""
    tempColor:list[str] = []
    tempActions:list[widgets.TripleButton] = [] #liste de classe Action (qui permet de reconfigurer l'ordre des actions d'un bandit)


    #liste "stockant" ce qui est dessiné sur un Canvas (afin de les pouvoir les supprimer par la suite)
    imgsOnCanvasPlaySpace:list[int] = []




    def __init__(self):
        super().__init__()

        #window parameters
        self.title('Colt Zeʁma')
        self.geometry('900x415')
        self.config(bg=Game.WIDGET_COLORS['sand'])

        #configures row/column weight, to make Canvas expands inside all window's space
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        #icon de l'application
        img = images.createLoadedImg(128, 128, images.imgIcon)
        self.call('wm', 'iconphoto', self._w, img)


        #variables de choix des actions
        self.currentTurn = 1
        self.action = 1 #only used to insert in Log while Actions phase
        self.banditQuiChoisi = 0
        self.soundsToPlay:str = [] #shoot, shootMissed, magEmpty, marshallShoot, walk, lootButin, lootMagot

        self.marshallDirection = 'right'


        # createMainMenu
        menus.createMainMenu(self)
        audios.setGlobalVolume(Game.VOLUME_GLOBAL)
        audios.setVolume('music', Game.VOLUME_MUSIC)
        audios.playMusic('main')



    #called by the command of a Scale
    def updateMusicVolume(self, value):
        value = int(value)
        Game.VOLUME_MUSIC = value
        audios.setVolume('music', value)

    #called by the command of a Scale
    def updateSoundsVolume(self, value):
        value = int(value)
        Game.VOLUME_SOUNDS = value
        audios.setVolume('sounds', value)




    #VALIDATION/LOG/OTIONS CANVAS CREATION =======================================

    def clearEntry(self):
        self.entryName.delete(0, END)



    #the next two fonctions are used to force the Frame (self.color) to always expand on same width
    def fillColorSpace(self, colors):
        for i, color in enumerate(colors):
            rb = Radiobutton(self.colorSpace, text=color, value=color, variable=self.selected_color, fg=tools.convertToHtml(Game.COLORS[color]))
            rb.config(bg='cadet blue', selectcolor='cadet blue', highlightthickness=0, activebackground=Game.WIDGET_COLORS['road'], activeforeground=Game.WIDGET_COLORS['train'])
            if i == len(colors)-1 and i%2 == 0:
                rb.grid(row=i%2, column=i//2, rowspan=2, sticky='nsew')
            else:
                rb.grid(row=i%2, column=i//2, sticky='nsew')


    def clearColorSpace(self):
        for radioButton in self.colorSpace.grid_slaves():
            radioButton.destroy()
        self.after(ms=100, func=lambda:self.fillColorSpace(self.tempColor))


    def fillActionsSpace(self):
        for _ in range(Game.MAX_ACTIONS):
            self.addActionToTempActions('osef')

        self.btnAction.config(text=f'Choose {Game.MAX_ACTIONS} actions...')

        self.after(ms=100, func=self.clearTempActions)



    def createValidationSpace(self):
        self.logSpace.grid_forget()

        #create Frame
        self.validationSpace = Canvas(self.menuSpace, bg=Game.WIDGET_COLORS['sand'], highlightthickness=0, border=0)
        for i in [0, 2]:
            self.validationSpace.columnconfigure(i, weight=1)
        for i in [0, 6]:
            self.validationSpace.rowconfigure(i, weight=1)
        self.validationSpace.grid(row=8, column=0, columnspan=5, sticky='news')


        self.nbTurnForLabel = StringVar()
        self.nbTurnForLabel.set(f'Turn {self.currentTurn}/{Game.NB_TOURS}')


        #create widgets (label, entry, colorsSpace, ActionsSpace, button)
        self.labelTurn = Label(self.validationSpace, textvariable=self.nbTurnForLabel)
        self.actionsSpace = Frame(self.validationSpace,bg=Game.WIDGET_COLORS['train'])
        self.btnValidate = Button(self.validationSpace, text='Validate', command=self.appendActionsToBandit, state='disabled')

        #widgets configuration
        self.labelTurn.config(justify='center', bg=Game.WIDGET_COLORS['sand'], fg=Game.WIDGET_COLORS['train'])
        self.actionsSpace.config(highlightthickness=2, border=0, highlightbackground=Game.WIDGET_COLORS['train'])
        self.btnValidate.config(highlightthickness=0, border=2, bg=Game.WIDGET_COLORS['train'], fg=Game.WIDGET_COLORS['road'], activebackground=Game.WIDGET_COLORS['road'], activeforeground=Game.WIDGET_COLORS['train'], disabledforeground=Game.WIDGET_COLORS['moutainShadow'])

        self.actionsSpace.rowconfigure(0, weight=1)
        for i in range(Game.MAX_ACTIONS):
            self.actionsSpace.columnconfigure(i, weight=1)

        #widgets placement
        self.labelTurn.grid(row=1, column=0, pady=2)
        self.actionsSpace.grid(row=4, column=0, sticky='ew', pady=2)
        self.btnValidate.grid(row=5, column=0, pady=2)


        #add widgets for the first turn (Frame for colors (RadioButtons) and Entry for Name)
        if self.currentTurn == 1:
            self.selected_color = StringVar()
            self.selected_color.set(False)

            #create widgets (label, entry, colorsSpace, ActionsSpace, button)
            self.entryName = Entry(self.validationSpace, width=40, justify='center', borderwidth=2)
            self.colorSpace = Frame(self.validationSpace, bg='cadet blue')

            #widgets configuration
            widgets.configWidgets(self, 'Entry', [self.entryName])
            self.entryName.config(width=40, justify='center')
            self.entryName.insert(0, '<Enter your name>')
            self.entryName.bind('<FocusIn>', lambda e:self.clearEntry())

            for i in [0, 1]:
                self.colorSpace.rowconfigure(i, weight=1)
            for i in range((len(self.tempColor) // 2)):
                self.colorSpace.columnconfigure(i, weight=1)
            if len(self.tempColor) % 2 == 1:
                self.colorSpace.columnconfigure((len(self.tempColor)//2), weight=1)

            #temporary fill colorSpace
            self.fillColorSpace(list(Game.COLORS.keys()))
            self.after(ms=100, func=self.clearColorSpace)

            #widgets placement
            self.entryName.grid(row=2, column=0, pady=2)
            self.colorSpace.grid(row=3, column=0, sticky='ew', pady=2)


        #add widgets for all other turns (2 Label for turn and Name)
        elif self.currentTurn > 1: #on n'a pas besoin de redonner un nom et choisir un couleur
            self.banditNameForLabel = StringVar()
            self.banditNameForLabel.set(f'{self.bandits[self.banditQuiChoisi].name}')

            #widgets creations
            self.labelName = Label(self.validationSpace, textvariable=self.banditNameForLabel, justify='center')

            #widgets configurations
            color = Game.bandits[self.banditQuiChoisi].colorHtml
            self.labelName.config(justify='center', bg=color, fg=Game.WIDGET_COLORS['train'])

            #widgets placements
            self.labelName.grid(row=2, rowspan=2, sticky='ew', pady=2)


        #place and remove an Action (so that actionsSpace expand in height)
        self.after(ms=100, func=self.fillActionsSpace)
    



    def createCanvasLog(self):
        self.logSpace = Canvas(self.menuSpace, border=0)
        self.logSpace.grid(row=8, column=0, columnspan=5)

        for i in [0, 3]:
            self.logSpace.columnconfigure(i, weight=1)
        for i in [0, 3]:
            self.logSpace.rowconfigure(i, weight=1)


        #widgets creation
        self.logLabel = Label(self.logSpace, text='History', font=('Ariel', 12), fg=Game.WIDGET_COLORS['sand'], bg=Game.WIDGET_COLORS['train'])
        self.logText = Text(self.logSpace, font=('Ariel', 10), highlightthickness=1, border=0, highlightbackground=Game.WIDGET_COLORS['train'], bg=Game.WIDGET_COLORS['sand'])
        logScrollbal = Scrollbar(self.logSpace, orient=VERTICAL, bg=Game.WIDGET_COLORS['train'], highlightthickness=1, border=0, highlightbackground=Game.WIDGET_COLORS['train'], activebackground=Game.WIDGET_COLORS['red'], troughcolor=Game.WIDGET_COLORS['sand'], width=15)


        #widgets configuration
        logScrollbal.config(command=self.logText.yview)
        self.logText.config(yscrollcommand=logScrollbal.set)

        self.logText.config(state=DISABLED)


        #widgets placement
        self.logLabel.grid(row=1, column=1, columnspan=2, sticky='nsew')
        self.logText.grid(row=2, column=1, sticky='nsew')
        logScrollbal.grid(row=2, column=2, sticky='NS')



    def destroyCanvasOptions(self):
        widgets.destroyWidgets([self.optionsSpace, self.labelPause])
        audios.resetMusicVolume(Game.VOLUME_MUSIC)
        


    def createCanvasOptions(self):
        audios.reduceMusicVolume(Game.VOLUME_MUSIC)
        self.optionsSpace = Canvas(self, bg=Game.WIDGET_COLORS['redLight'], highlightthickness=2, border=0, highlightbackground=Game.WIDGET_COLORS['red'])
        self.optionsSpace.grid(row=0, column=1, sticky='news')

        for i in [0, 3]:
            self.optionsSpace.columnconfigure(i, weight=1)
        for i in [0, 8]:
            self.optionsSpace.rowconfigure(i, weight=4)
        for i in [2, 4, 6]:
            self.optionsSpace.rowconfigure(i, weight=1)

        #widgets creations
        self.labelPause = Label(self.playSpace, text="PAUSE", font=40)
        self.btnClose = Button(self.optionsSpace, text='Return to Game', command=self.destroyCanvasOptions)
        self.btnSave = Button(self.optionsSpace, text='Save', command=self.confirmSaveGame)
        self.btnReturnToMainMenu = Button(self.optionsSpace, text='Main Menu', command=self.confirmReturnToMainMenu)
        self.btnExit = Button(self.optionsSpace, text='Exit', command=self.confirmExitGame)

        #widgets configuration
        for i in [0, 2]:
            self.playSpace.columnconfigure(i, weight=1)
            self.playSpace.rowconfigure(i, weight=1)
        self.playSpace.rowconfigure(2, weight=6)

        widgets.configWidgets(self, 'Label', [self.labelPause])
        widgets.configWidgets(self, 'Button', [self.btnClose, self.btnSave, self.btnReturnToMainMenu, self.btnExit])

        #widgets placement
        self.labelPause.grid(row=1, column=1)

        self.btnClose.grid(row=1, column=1, columnspan=2)
        self.btnSave.grid(row=3, column=1, columnspan=2, sticky='we')
        self.btnReturnToMainMenu.grid(row=5, column=1, columnspan=2, sticky='we')
        self.btnExit.grid(row=7, column=1, columnspan=2, sticky='we')

        if not len(self.bandits) == Game.NB_JOUEURS:
            self.btnSave.config(state='disabled')
        else:
            self.btnSave.config(state='normal')
    
    #FIN === VALIDATION/LOG/OTIONS CANVAS CREATION =================================



    #mise à jour des variables globales (avant de continuer à process)
    def startGame(self, canvasToDestroy:Canvas, nbPlayers=4, nbWagons=4, nbTurns=3, nbActions=6, minButins=1, maxButins=4, nbBullets=12, loadSave=False):
        canvasToDestroy.destroy()
        audios.fadeOutMusic(3000)
        audios.playSound('startGame')

        #reset variables
        self.wagons.clear()
        self.bandits.clear()
        self.butins.clear()
        self.tempName = ""
        self.tempColor.clear()
        self.tempActions.clear()


        #fill tempColor
        for color in Game.COLORS:
            Game.tempColor.append(color)


        #update globales
        if loadSave:
            Game.LOAD_SAVE = True

        else:
            Game.LOAD_SAVE = False

            Game.NB_JOUEURS = nbPlayers
            Game.NB_WAGONS = nbWagons
            Game.NB_TOURS = nbTurns
            Game.MAX_ACTIONS = nbActions
            Game.MIN_BUTINS = minButins
            Game.MAX_BUTINS = maxButins
            Game.MAX_BULLETS = nbBullets

            self.currentTurn = 1


        self.action = 1 #only used to insert in Log while Actions phase
        self.banditQuiChoisi = 0
        
        self.continueInit()
        


    def continueInit(self):
        self.canvasMainMenu.destroy()

        #la fenêtre est coupée en 2 parties :
        #    playSpace: Canvas sur lequel on dessine l'aspect visuel du jeu (bg, train, personnages...)
        #    menuSpace: Canvas sur lequel on interagit avec le jeu (bouttons d'action, log, save, exit...)


        #=== PLAY SPACE ====================================
        self.playSpace = Canvas(self, highlightthickness=0, bg=Game.WIDGET_COLORS['train'])
        self.playSpace.grid(row=0, column=0, sticky='nsew')

        #resize des images de l'interface lorsque la fenêtre est redimensionnée
        self.playSpace.bind('<Configure>', lambda e: self.updateCanvasImgs())

        #=== FIN PLAY SPACE ================================


        #=== MENU SPACE ====================================
        self.menuSpace = Canvas(self, bg=Game.WIDGET_COLORS['redLight'], highlightthickness=2, border=0, highlightbackground=Game.WIDGET_COLORS['red'])
        self.menuSpace.grid(row = 0, column= 1, sticky='nsew')

        for i in [0, 5, 7]:
            self.menuSpace.rowconfigure(i, weight=1)

        for i in [0, 4]:
            self.menuSpace.columnconfigure(i, weight=1)


        self.menuSpaceBtns = []

        #boutons
        self.btnAction = Button(self.menuSpace, text='Action', command=self.executeTurn, highlightthickness=0)
        self.btnOptions = Button(self.menuSpace, text='+', command=self.createCanvasOptions)

        self.btnRight = Button(self.menuSpace, text='->', command=lambda:self.addActionToTempActions('right'))
        self.btnLeft = Button(self.menuSpace, text='<-', command=lambda:self.addActionToTempActions('left'))
        self.btnUp = Button(self.menuSpace, text='Up', command=lambda:self.addActionToTempActions('up'))
        self.btnDown = Button(self.menuSpace, text='Down', command=lambda:self.addActionToTempActions('down'))
        self.btnShoot = Button(self.menuSpace, text='Shoot', command=lambda:self.addActionToTempActions('shoot'))
        self.btnSteal = Button(self.menuSpace, text='Rob', command=lambda:self.addActionToTempActions('rob'))
        

        self.menuSpaceBtns.append(self.btnRight)
        self.menuSpaceBtns.append(self.btnLeft)
        self.menuSpaceBtns.append(self.btnUp)
        self.menuSpaceBtns.append(self.btnDown)
        self.menuSpaceBtns.append(self.btnShoot)
        self.menuSpaceBtns.append(self.btnSteal)

        #config buttons (except 'btnAction')
        widgets.configWidgets(self, 'Button', [self.btnOptions])
        for btn in self.menuSpaceBtns:
            btn.config(bg=Game.WIDGET_COLORS['redLight'], border=0, highlightthickness=0, activebackground=Game.WIDGET_COLORS['red'])


        #placement des buttons
        self.btnAction.grid(row=6, column=2, padx=5, pady=10)
        self.btnOptions.grid(row=1, column=3, sticky='ne')

        self.btnRight.grid(row=2, column=3, rowspan=2)
        self.btnLeft.grid(row=2, column=1, rowspan=2)
        self.btnUp.grid(row=1, column=2)
        self.btnDown.grid(row=4, column=2)
        self.btnShoot.grid(row=2, column=2)
        self.btnSteal.grid(row=3, column=2)


        #actions history
        self.createCanvasLog()

        #=== FIN MENU SPACE ================================



        #création des wagons, personnages et butins

        #create from new game
        if not Game.LOAD_SAVE:
            #création des wagons
            for y in range(Game.NB_WAGONS + 1):
                #loco
                if y == 0:
                    self.wagons.append(Wagon(self, y, 'loco'))
                    continue
                #queue
                if y == Game.NB_WAGONS:
                    self.wagons.append(Wagon(self, y, 'queue'))
                    continue
                #wagon
                self.wagons.append(Wagon(self, y, 'wagon'))


            #ajout du marshall
            self.wagons[0].marshall = True

            self.btnAction.config(text=f'Choose {Game.MAX_ACTIONS} actions...')
            widgets.configActionButton(self, 'preparation')
            self.createValidationSpace()


        #create from loaded game
        else:
            #import save
            Game.NB_JOUEURS, Game.NB_TOURS, self.currentTurn, Game.NB_WAGONS, Game.MAX_ACTIONS, self.marshallDirection, preparation, tempWagons, tempBandits, tempButins = saveGestion.loadSave()


        # 0:number of players-------
        # 1:number of turns---------
        # 2:current turn---------
        # 3:number of wagons---------
        # 4:max number of actions---------
        # 5:preparation(bool)
        # 6:number of butins (dont return)



            #load Wagon(s)
            for wagonElement in tempWagons:
                xPos = wagonElement[0]
                type = wagonElement[1]
                marshall = wagonElement[2]

                loadedWagon = Wagon(self, xPos, type, marshall=marshall)
                self.wagons.append(loadedWagon)

            #load Bandit(s)
            for banditElements in tempBandits:
                name = banditElements[0]
                color = banditElements[1]
                xPos, yPos = banditElements[2], banditElements[3]
                actions = banditElements[4:-1]
                bullets = banditElements[-1]

                loadedBandit = Bandit(self, name, color, position=(xPos, yPos), actions=actions, bullets=bullets)
                self.bandits.append(loadedBandit)

            #load Butin(s)
            for butinElements in tempButins:
                type = butinElements[0]
                value = butinElements[1]
                xPos, yPos = butinElements[2], butinElements[3]
                bracable = butinElements[4]

                Butin(self, type, None, value=value, position=(xPos, yPos), bracable=bracable)
                # le Butin s'auto append dans self.butins


            # butins' distribution
            for butin in self.butins:
                #in a Wagon
                if butin.position['y'] in ['in', 'out']:
                    self.wagons[butin.position['x']].butins.append(butin)
                
                #in a Bandit
                else:
                    for bandit in self.bandits:
                        if bandit.name == butin.position['y']:
                            bandit.butins.append(butin)
                            break



            if preparation:
                self.btnAction.config(text=f'Choose {Game.MAX_ACTIONS} actions...')
                widgets.configActionButton(self, 'preparation')
                self.createValidationSpace()
            else:
                self.btnAction.config(text='Action !')
                widgets.configActionButton(self, 'action')
                for btn in self.menuSpaceBtns:
                    btn.config(state='disabled')

                self.insertTextInLog('\n\nGame succesfully loaded\n')
                self.insertTextInLog(f'\n\n\n=== Turn {self.currentTurn}/{Game.NB_TOURS}===\n')
            
            self.action = Game.MAX_ACTIONS - len(Game.bandits[0].actions) + 1

        menus.createLoadingScreen(self, 'maria')
        

    """
    
    self.btnClose
    self.btnSave
    self.btnReturnToMainMenu
    self.btnExit
    """

    def saveGame(self):
        if len(self.bandits[-1].actions) == 0:
            preparation = True
        else:
            preparation = False

        saveGestion.save(Game.NB_JOUEURS, Game.NB_TOURS, self.currentTurn, Game.NB_WAGONS, Game.MAX_ACTIONS, self.marshallDirection, preparation, self.wagons, self.bandits, self.butins)

        self.destroyCanvasOptions()

        self.insertTextInLog('\n\nGame succesfully saved\n')



    def confirmSaveGame(self):
        self.btnSave.grid_forget()
        audios.playSound('confirm')
        
        self.btnClose.config(state='disabled')
        self.btnReturnToMainMenu.config(state='disabled')
        self.btnExit.config(state='disabled')

        self.btnYes = Button(self.optionsSpace, text='Yes', command=self.saveGame)
        self.btnNo = Button(self.optionsSpace, text='No', command=lambda:self.cancelConfirmation(self.btnSave, 3))

        widgets.configWidgets(self, 'Button', [self.btnYes, self.btnNo])

        self.btnYes.grid(row=3, column=1, sticky='we')
        self.btnNo.grid(row=3, column=2, sticky='we')



    def confirmReturnToMainMenu(self):
        self.btnReturnToMainMenu.grid_forget()
        audios.playSound('confirm')
        
        self.btnClose.config(state='disabled')
        self.btnSave.config(state='disabled')
        self.btnExit.config(state='disabled')

        self.btnYes = Button(self.optionsSpace, text='Yes', command=lambda:menus.returnToMainMenu(self, [self.playSpace, self.menuSpace, self.optionsSpace, self.labelPause], fromGame=True))
        self.btnNo = Button(self.optionsSpace, text='No', command=lambda:self.cancelConfirmation(self.btnReturnToMainMenu, 5))

        widgets.configWidgets(self, 'Button', [self.btnYes, self.btnNo])

        self.btnYes.grid(row=5, column=1, sticky='we')
        self.btnNo.grid(row=5, column=2, sticky='we')
    


    def confirmExitGame(self):
        self.btnExit.grid_forget()
        audios.playSound('confirm')
        
        self.btnClose.config(state='disabled')
        self.btnSave.config(state='disabled')
        self.btnReturnToMainMenu.config(state='disabled')

        self.btnYes = Button(self.optionsSpace, text='Yes', command=self.destroy)
        self.btnNo = Button(self.optionsSpace, text='No', command=lambda:self.cancelConfirmation(self.btnExit, 7))

        widgets.configWidgets(self, 'Button', [self.btnYes, self.btnNo])

        self.btnYes.grid(row=7, column=1, sticky='we')
        self.btnNo.grid(row=7, column=2, sticky='we')
    


    def cancelConfirmation(self, btn:Button, row:int):
        audios.playSound('cancel')
        widgets.destroyWidgets([self.btnYes, self.btnNo])
        
        self.btnClose.config(state='normal')
        self.btnReturnToMainMenu.config(state='normal')
        self.btnExit.config(state='normal')


        if not len(self.bandits) == Game.NB_JOUEURS:
            self.btnSave.config(state='disabled')
        else:
            self.btnSave.config(state='normal')


        btn.grid(row=row, column=1, columnspan=2, sticky='we')





    def addActionToTempActions(self, action:str):
        actionbtn = widgets.TripleButton(self, self.actionsSpace, action, len(Game.tempActions))
        Game.tempActions.append(actionbtn)

        #si toutes les actions ont été données
        if len(Game.tempActions) == Game.MAX_ACTIONS:
            if self.currentTurn == 1:
                #check if Name or Color datas are missing
                if self.entryName.get() in ["", '<Enter your name>'] or not self.selected_color.get() in Game.tempColor:
                    self.btnAction.config(text='Name or Color are missing')
            
            else:
                self.btnAction.config(text='Press "Validate"')


        self.updateActionsBar()
        self.updateCanvasImgs()
        



    def removeAction(self, actionToRemove:widgets.TripleButton):
        founded = False
        for action in Game.tempActions:
            if founded:
                action.column -= 1
                continue
            if action == actionToRemove:
                founded = True

        if not founded:
            print('ERROR: in colt-ze3ma.py in removeAction:\n  action not found')
            exit()

        Game.tempActions.remove(actionToRemove)
        self.btnAction.config(text=f'Choose {Game.MAX_ACTIONS} actions...')
        self.updateActionsBar()



    def updateActionsBar(self):
        #clear actions bar
        for widget in self.actionsSpace.grid_slaves(row=0):
            widget.grid_remove()
        
        #fill it
        for action in Game.tempActions:
            action.grid(row=0, column=action.column)
            action.drawImg()

        #update buttons state
        if len(Game.tempActions) == Game.MAX_ACTIONS: #nombre d'actions atteint
            self.btnValidate.config(state='normal')
            for btn in self.menuSpaceBtns:
                btn.configure(state='disabled')
        else: #il n'y a pas assez d'actiions
            self.btnValidate.config(state='disabled')
            for btn in self.menuSpaceBtns:
                btn.configure(state='normal')



    def clearTempActions(self):
        for widget in self.actionsSpace.grid_slaves(row=0):
            widget.grid_remove()

        Game.tempActions.clear()
        self.updateActionsBar()



    def appendActionsToBandit(self):
        #check if all data are given on the first turn
        if self.currentTurn == 1:
            #do nothing if name or color are missing
            if self.entryName.get() in ["", '<Enter your name>']:
                self.btnAction.config(text='Name is missing')
                return
            if not self.selected_color.get() in Game.tempColor:
                self.btnAction.config(text='Color is missing')
                return


        #préparation des actions à donner au Bandit (parceque Bandit reçoit une list(str), et non une list(Action))
        tempActions = []
        for actionBtn in Game.tempActions:
            tempActions.append(actionBtn.value)


        #check of new Bandits must be create, or if we must add actions in already existing Bandits
        if self.currentTurn == 1: #on créé un nouveau Bandit
            bandit = Bandit(self, self.entryName.get(), self.selected_color.get(), actions=tempActions)
            self.bandits.append(bandit)

        else: #append les actions dans un bandit
            self.bandits[self.banditQuiChoisi].actions = tempActions


        self.banditQuiChoisi += 1
        Game.tempActions.clear()


        if self.banditQuiChoisi == Game.NB_JOUEURS: #tous les joueurs ont selectionnés leurs actions
            self.btnAction.config(state='normal', text='Action !')
            widgets.configActionButton(self, 'action')
            for btn in self.menuSpaceBtns:
                btn.config(state='disabled')

            self.banditQuiChoisi = 0
            self.action = 1
            self.validationSpace.grid_forget()
            self.logSpace.grid(row=8, column=0, columnspan=5)

            self.insertTextInLog(f'\n\n\n=== Turn {self.currentTurn} ===\n')
            

        else: #d'autres joueurs doivent encore choisir leur actions
            self.btnValidate.config(state='disabled')
            for btn in self.menuSpaceBtns:
                btn.config(state='normal')

            #reset Name and Color values of Validation Canvas
            if self.currentTurn == 1:
                self.tempColor.remove(self.selected_color.get())
                self.entryName.delete(0,END)

            #suppression et recréation du Validation Canvas
            self.validationSpace.grid_forget()
            self.createValidationSpace()

            if self.currentTurn > 1:
                self.labelName.config(bg=Game.bandits[self.banditQuiChoisi].colorHtml)

    



    def moveMarshall(self):
        xWagonPosition = 0 #position du wagon où se trouve le Marshall
        for wagon in self.wagons:
            if wagon.marshall == True:
                xWagonPosition = wagon.xPosition
                break

        #Marshall en tête de train
        if xWagonPosition == 0:
            self.marshallDirection = 'right'
            self.wagons[xWagonPosition].marshall = False
            self.wagons[xWagonPosition + 1].marshall = True
            return

        #Marshall en queue de train
        elif xWagonPosition == Game.NB_WAGONS:
            self.marshallDirection = 'left'
            self.wagons[xWagonPosition].marshall = False
            self.wagons[xWagonPosition - 1].marshall = True
            return

        #Marshall ni en tête/queue du train, donc on le déplace aléatoirement
        directions = []
        for _ in range(8):
            directions.append(self.marshallDirection)
        if self.marshallDirection == 'right':
            for _ in range(2):
                directions.append('left')
        elif self.marshallDirection == 'left':
            for _ in range(2):
                directions.append('right')


        direction = random.choice(directions)

        if direction == 'right':
            self.marshallDirection = 'right'
            self.wagons[xWagonPosition].marshall = False
            self.wagons[xWagonPosition + 1].marshall = True

        elif direction == 'left':
            self.marshallDirection = 'left'
            self.wagons[xWagonPosition].marshall = False
            self.wagons[xWagonPosition - 1].marshall = True







    def insertTextInLog(self, text:str, color=WIDGET_COLORS['train']):
        tagName = 'color-' + color
        self.logText.tag_configure(tagName, foreground=color)
        self.logText.config(state='normal')
        self.logText.insert(END, text, tagName)
        self.logText.see(END)
        self.logText.config(state='disabled')




    def defineSoundsToPlay(self):
        self.soundsToPlay = list(set(self.soundsToPlay))



    def playSoundWalk(self, step=3):
        if step == 0:
            return

        audios.playSound('stepSide')
        self.after(ms=200, func=lambda:self.playSoundWalk(step=step-1))


    def playSoundWalkMarshall(self, step=2):
        if step == 0:
            return

        audios.playSound('stepSide')
        self.after(ms=375, func=lambda:self.playSoundWalk(step=step-1))



    #play Sounds for step (on 4) of a turn, then continu to executeTurn
    def playSounds(self, executeTurnStep):
        # audios.playSound('returnMainMenu')
        if 'shoot' in self.soundsToPlay:
            self.soundsToPlay.remove('shoot')
            audios.playSound('shoot')
            self.after(ms=400, func=lambda:self.playSounds(executeTurnStep))
            return
        if 'shootMissed' in self.soundsToPlay:
            self.soundsToPlay.remove('shootMissed')
            audios.playSound('returnMainMenu')
            self.after(ms=400, func=lambda:self.playSounds(executeTurnStep))
            return
        if 'magEmpty' in self.soundsToPlay:
            self.soundsToPlay.remove('magEmpty')
            audios.playSound('shootEmpty')
            self.after(ms=400, func=lambda:self.playSounds(executeTurnStep))
            return
        if 'marshallShoot' in self.soundsToPlay:
            self.soundsToPlay.remove('marshallShoot')
            audios.playSound('marshallShoot')
            self.after(ms=400, func=lambda:self.playSounds(executeTurnStep))
            return
        if 'walk' in self.soundsToPlay:
            self.soundsToPlay.remove('walk')
            self.playSoundWalk()
            self.after(ms=600, func=lambda:self.playSounds(executeTurnStep))
            return
        if 'walkMarshall' in self.soundsToPlay:
            self.soundsToPlay.remove('walkMarshall')
            self.playSoundWalkMarshall()
            self.after(ms=600, func=lambda:self.playSounds(executeTurnStep))
            return
        if 'lootButin' in self.soundsToPlay:
            self.soundsToPlay.remove('lootButin')
            audios.playSound('butin')
            self.after(ms=400, func=lambda:self.playSounds(executeTurnStep))
            return
        if 'lootMagot' in self.soundsToPlay:
            self.soundsToPlay.remove('lootMagot')
            audios.playSound('magot') 
            self.after(ms=400, func=lambda:self.playSounds(executeTurnStep))
            return
        
        # self.executeTurn(executeTurnStep)
        if executeTurnStep == 2:
            self.after(ms=100, func=lambda:self.executeTurn(executeTurnStep))
        elif executeTurnStep == 3:
            self.after(ms=500, func=lambda:self.executeTurn(executeTurnStep))
        elif executeTurnStep == 4:
            self.after(ms=100, func=lambda:self.executeTurn(executeTurnStep))


    def executeTurn(self, step=1):
        if step == 1:
            #check if its the end of the turn/game
            if self.btnAction['text'] == 'End Game !':
                self.determineWinner()
                return

            elif self.btnAction['text'] == 'End Turn !':
                self.action = 1
                self.currentTurn += 1
                self.createValidationSpace()

                self.btnAction.config(text=f'Choose {Game.MAX_ACTIONS} actions...')
                widgets.configActionButton(self, 'preparation')

                for btn in self.menuSpaceBtns:
                    btn.config(state='disabled')
                return


            
            #temporary disable Action button
            self.btnAction.config(state='disabled', text='Wait...')

            #add recap turn/action state in Log
            self.insertTextInLog(f'\nTurn {self.currentTurn}/{Game.NB_TOURS}\n')
            self.insertTextInLog(f'Action {self.action}/{Game.MAX_ACTIONS}\n')
            self.action += 1

            #execute l'action de chaque bandit
            for bandit in Game.bandits:
                bandit.executeAction()

            self.updateCanvasImgs()
            self.defineSoundsToPlay()
            self.playSounds(step+1)
            # self.after(ms=100, func=lambda:self.executeTurn(step=step+1))
        

        elif step == 2:
            #verifie pour chaque bandit s'il le Marshall est au même endroit (déplace le bandit si oui)
            for bandit in Game.bandits:
                bandit.checkMarshallPresence()

            #update du Canvas
            self.updateCanvasImgs()
            self.defineSoundsToPlay()
            self.playSounds(step+1)
            # self.after(ms=500, func=lambda:self.executeTurn(step=step+1))


        elif step == 3:
            #déplace le marshall
            self.moveMarshall()
            self.soundsToPlay.append('walkMarshall')

            #update du Canvas
            self.updateCanvasImgs()
            self.defineSoundsToPlay()
            self.playSounds(step+1)
            # self.after(ms=100, func=lambda:self.executeTurn(step=step+1))


        elif step == 4:
            #verifie pour chaque bandit s'il le Marshall est au même endroit (déplace le bandit si oui)
            for bandit in Game.bandits:
                bandit.checkMarshallPresence()

            #update du Canvas
            self.updateCanvasImgs()
            self.defineSoundsToPlay()
            self.playSounds(step+1)

            self.btnAction.config(state='normal', text='Action !')

            #check if its the end of the turn/game
            if not len(self.bandits[0].actions):
                if self.currentTurn == Game.NB_TOURS: #end of game
                    self.btnAction.config(text='End Game !')

                #end of turn
                else:
                    self.btnAction.config(text='End Turn !')





    def determineWinner(self):
        indexWinners:list[int] = []
        highestMoneyAmount = 0
        playersNameAndResult:list[list[str]] = [[], []]

        for i, bandit in enumerate(self.bandits):
            playersNameAndResult[0].append(bandit.name)
            playersNameAndResult[1].append(bandit.formatedStr())

            tempMoneyAmount = 0
            for butin in bandit.butins:
                tempMoneyAmount += butin.value

            if tempMoneyAmount == highestMoneyAmount:
                indexWinners.append(i)
            elif tempMoneyAmount > highestMoneyAmount:
                indexWinners.clear()
                indexWinners.append(i)
                highestMoneyAmount = tempMoneyAmount

        # saveGestion.emptySave()
        menus.createEndGameMenu(self, indexWinners, playersNameAndResult)
        menus.createLoadingScreen(self, 'main')


























    def createInventoryCanvas(self, bandit:Bandit, widthplaySpace:int, heightplaySpace:int, xOffset:int, index:int):
        #taille de l'inventaire
        widthInventorySize = widthplaySpace//8
        heightInventorySize = heightplaySpace//4

        #position de l'inventaire
        xPlacementPosition = ((widthplaySpace//Game.NB_JOUEURS)*index) + (((widthplaySpace//Game.NB_JOUEURS)//2) - widthInventorySize//2)
        yPlacementPosition = int(heightplaySpace*0.71)

        #taille des icones (de la tête du bandit en réalité, les autres sont 2* plus petit)
        widthIcon = widthInventorySize
        heightIcon = heightInventorySize//2


        #création des images
        bandit.imgHead = images.createBanditPng(widthIcon, heightIcon, Game.COLORS[bandit.color], justHead=True)
        bandit.imgMunition = images.createLoadedImg(widthIcon//2, heightIcon//2, images.imgIconMinution)
        bandit.imgBourse = images.createLoadedImg(widthIcon//2, heightIcon//2, images.imgIconBourse)
        nbMunitions = bandit.bullets
        nbBourses = len(bandit.butins)

        #placement des images
        imgHead = self.playSpace.create_image(xOffset + xPlacementPosition, yPlacementPosition, image=bandit.imgHead, anchor='nw')
        imgBullet = self.playSpace.create_image(xOffset + xPlacementPosition, yPlacementPosition + heightIcon, image=bandit.imgMunition, anchor='nw')
        imgBourse = self.playSpace.create_image(xOffset + (xPlacementPosition + (widthIcon//2)), yPlacementPosition + heightIcon, image=bandit.imgBourse, anchor='nw')

        #placement du texte
        xTextOffset = widthIcon//4
        yTextOffset = heightIcon//4

        x = xPlacementPosition + ((xTextOffset) - (xTextOffset*0.2))
        y = yPlacementPosition + (((heightIcon//2)*3) + (yTextOffset*0.2))
        imgNbBullets = self.playSpace.create_text(xOffset + x, y, text=str(nbMunitions), anchor='nw')

        x = xPlacementPosition + (((widthIcon//2) + xTextOffset) - (xTextOffset*0.2))
        y = yPlacementPosition + (((heightIcon//2)*3) + (yTextOffset*0.2))
        imgNbBourses = self.playSpace.create_text(xOffset + x, y, text=str(nbBourses), anchor='nw')

        #mise des dessins dans la liste globale
        self.imgsOnCanvasPlaySpace.append(imgHead)
        self.imgsOnCanvasPlaySpace.append(imgBullet)
        self.imgsOnCanvasPlaySpace.append(imgBourse)
        self.imgsOnCanvasPlaySpace.append(imgNbBullets)
        self.imgsOnCanvasPlaySpace.append(imgNbBourses)





    def updateCanvasImgs(self):
        #ON VIDE LE CANVAS ===================================
        for img in self.imgsOnCanvasPlaySpace:
            self.playSpace.delete(img)
        self.imgsOnCanvasPlaySpace.clear()


        #taille du Canvas
        widthCanvas = self.playSpace.winfo_width()
        heightCanvas = self.playSpace.winfo_height()
        widthDrawingSpace = widthCanvas
        heightDrawingSpace = heightCanvas
        xOffsetCanvas = 0
        yOffsetCanvas = 0

        widthRatio = Game.NB_WAGONS + 2
        heightRatio = 3

        #check ratio respect
        width = widthCanvas // widthRatio
        height = heightCanvas // heightRatio

        self.imgBackgroundSafe = None

        if width > height: #etiré dans la largeur
            # self.imgBackgroundSafe = images.createLoadedImg(widthDrawingSpace, heightDrawingSpace, images.imgPaysageSafeHeight)
            
            widthDrawingSpace = int(height * widthRatio)
            xOffsetCanvas = (self.playSpace.winfo_width()//2) - (widthDrawingSpace //2)

        elif width < height: #etiré dans la hauteur
            self.imgBackgroundSafe = images.createLoadedImg(widthDrawingSpace, heightDrawingSpace, images.imgPaysageSafeHeight)

            heightDrawingSpace = int(width * heightRatio)
            yOffsetCanvas = (self.playSpace.winfo_height()//2) - (heightDrawingSpace //2)

        img = self.playSpace.create_image(0, 0, image=self.imgBackgroundSafe, anchor='nw')
        self.imgsOnCanvasPlaySpace.append(img)


        #ON DÉFINI LES TAILLES DE TOUTES LES IMAGES ==========

        #taille d'un Wagon
        widthWagon = widthDrawingSpace // (Game.NB_WAGONS+1+1)
        heightWagon = heightDrawingSpace // 3
        #taille des personnages (marshall and Bandit)
        widthCharacter = int (widthWagon *0.26)
        heightCharacter = int (heightWagon *0.42)

        #taille des butins
        widthBourse = int(widthWagon * 0.13)
        heightBourse = int(heightWagon *  0.11)
        widthBijoux = int(widthWagon * 0.07)
        heightBijoux = int(heightWagon *  0.06)
        widthMagot = int(widthWagon * 0.35)
        heightMagot = int(heightWagon *  0.20)

        #taille des images de boutons
        # sizeButton = ((heightDrawingSpace//3) * 2) // 7
        sizeButton = (self.menuSpace.winfo_height() // 2) // 6



        #MENU SPACE =========================================
        #resize du log
        if len(self.bandits) and len(self.bandits[0].actions):
            self.logText.config(width=widthDrawingSpace//20, height=int((heightDrawingSpace//2)*0.08))

        #images des boutons
        self.imgTest = images.createLoadedImg(sizeButton, sizeButton, images.imgWagon)
        self.imgBtnRight = images.createLoadedImg(sizeButton, sizeButton, images.imgRight)
        self.imgBtnLeft = images.createLoadedImg(sizeButton, sizeButton, images.imgLeft)
        self.imgBtnUp = images.createLoadedImg(sizeButton, sizeButton, images.imgUp)
        self.imgBtnDown = images.createLoadedImg(sizeButton, sizeButton, images.imgDown)
        self.imgBtnShoot = images.createLoadedImg(sizeButton, sizeButton, images.imgShoot)
        self.imgBtnRob = images.createLoadedImg(sizeButton, sizeButton, images.imgRob)

        self.btnRight.config(image=self.imgBtnRight)
        self.btnLeft.config(image=self.imgBtnLeft)
        self.btnUp.config(image=self.imgBtnUp)
        self.btnDown.config(image=self.imgBtnDown)
        self.btnShoot.config(image=self.imgBtnShoot)
        self.btnSteal.config(image=self.imgBtnRob)


        #var 'img' will be used as a create_image() container

        #ON DESSINE LE BACKGROUND ============================
        self.imgPaysage = images.createLoadedImg(widthDrawingSpace, heightDrawingSpace, images.imgPaysage)
        img = self.playSpace.create_image(xOffsetCanvas, yOffsetCanvas, image=self.imgPaysage, anchor='nw')
        self.imgsOnCanvasPlaySpace.append(img)



        #ON DESSINE LES WAGONS ==============================
        self.imgLoco = images.createLoadedImg(widthWagon*2, heightWagon, images.imgLoco)
        self.imgWagon = images.createLoadedImg(widthWagon, heightWagon, images.imgWagon)
        self.imgQueue = images.createLoadedImg(widthWagon, heightWagon, images.imgQueue)

        #loco
        img = self.playSpace.create_image(xOffsetCanvas, yOffsetCanvas + heightWagon, image=self.imgLoco, anchor='nw')
        self.imgsOnCanvasPlaySpace.append(img)

        #wagon
        for xWagonPosition in range(1, Game.NB_WAGONS):
            img = self.playSpace.create_image(xOffsetCanvas + ((xWagonPosition +1)*widthWagon), yOffsetCanvas + heightWagon, image=self.imgWagon, anchor='nw')
            self.imgsOnCanvasPlaySpace.append(img)

        #queue
        img = self.playSpace.create_image(xOffsetCanvas + ((Game.NB_WAGONS +1)*widthWagon), yOffsetCanvas + heightWagon, image=self.imgQueue, anchor='nw')
        self.imgsOnCanvasPlaySpace.append(img)

        #FIN === ON DESSINE LES WAGONS =====================


        #ON DESSINE LES BUTINS DANS LES WAGONS ==============================
        for wagon in Game.wagons:
            nbButins = len(wagon.butins)

            if nbButins == 0:
                continue

            #une boucle juste pour le magot
            for butin in wagon.butins:
                if not butin.type == 'magot':
                    continue

                xButinPosition = butin.position['x']
                yButinPosition:str = butin.position['y']

                #les Offset permet de placer le butin au centre du wagon (sont ajustés par la suite)
                xOffsetButin = widthWagon + (widthWagon//2) - (widthMagot//2)
                yOffsetButin = (heightWagon-heightMagot) - (heightWagon * 0.35) #hauteaur à l'intérieur du wagon

                xImgPosition = (xButinPosition * widthWagon) + xOffsetButin

                if yButinPosition == 'in':
                    yImgPosition = heightWagon + yOffsetButin
                elif yButinPosition == 'out':
                    yImgPosition = yOffsetButin + (heightWagon * 0.40)
                else:
                    print('ERROR: in colt-ze3ma.py in updateCanvasImgs (butin, loop for magot):\n  the butin is in a wagon\'s list, but is own by a bandit')
                    exit()


                butin.img = images.createLoadedImg(widthMagot, heightMagot, images.imgMagot, flip=butin.flipImg)
                img = self.playSpace.create_image(xOffsetCanvas + xImgPosition, yOffsetCanvas + yImgPosition, image=butin.img, anchor='nw')
                self.imgsOnCanvasPlaySpace.append(img)

                break


            #une boucle pour les autres type de butins (sauf 'magot')
            for i in range(nbButins):
                butin = wagon.butins[i]

                xButinPosition = butin.position['x']
                yButinPosition:str = butin.position['y']


                if butin.type == 'magot':
                    continue
                    

                elif butin.type == 'bijoux':
                    #les Offset permet de placer le butin au centre du wagon (sont ajustés par la suite)
                    xOffsetButin = widthWagon + (widthWagon//2) - (widthBijoux//2)
                    yOffsetButin = (heightWagon-heightBijoux) - (heightWagon * 0.32) #hauteaur à l'intérieur du wagon

                    if butin.bracable == False:
                        #décalage selon le nombre de butins dans le même wagon
                        if (i % 2) == 1:
                            xOffsetButin += (((widthWagon*0.6) // nbButins) + ((i * ((widthWagon*0.6) // nbButins)))) //2

                        else:
                            xOffsetButin -= (((widthWagon*0.6) // nbButins) + ((i * ((widthWagon*0.6) // nbButins)))) //2

                        #décalage y
                        yOffsetButin -= (heightWagon*0.005) * (i%3) #réhaussement de 0.005% * 0 ou 1 ou 2

                    else: #bracable == True
                        #décalage selon le nombre de butins dans le même wagon
                        if (i % 2) == 1:
                            xOffsetButin += (((widthWagon*0.2) // nbButins) + ((i * ((widthWagon*0.2) // nbButins)))) //2

                        else:
                            xOffsetButin -= (((widthWagon*0.2) // nbButins) + ((i * ((widthWagon*0.2) // nbButins)))) //2

                        #décalage y
                        yOffsetButin -= heightWagon*0.2 #réhaussement pour le placer sur la table
                        yOffsetButin -= (heightWagon*0.005) * (i%3) #réhaussement de 1% * 0 ou 1 ou 2


                    xImgPosition = (xButinPosition * widthWagon) + xOffsetButin

                    if yButinPosition == 'in':
                        yImgPosition = heightWagon + yOffsetButin
                    elif yButinPosition == 'out':
                        yImgPosition = yOffsetButin + (heightWagon * 0.38)
                    else:
                        print('ERROR: in colt-ze3ma.py in updateCanvasImgs: (butin, loop for other then magot, bijoux)\n  the butin is in a wagon\'s list, but is own by a bandit')
                        exit()

                    


                elif butin.type == 'bourse':
                    #les Offset permet de placer le butin au centre du wagon (sont ajustés par la suite)
                    xOffsetButin = widthWagon + (widthWagon//2) - (widthBourse//2)
                    yOffsetButin = (heightWagon-heightBourse) - (heightWagon * 0.32) #hauteaur à l'intérieur du wagon

                    if butin.bracable == False:
                        #décalage x selon le nombre de butins dans le même wagon
                        if (i % 2) == 1:
                            xOffsetButin += (((widthWagon*0.6) // nbButins) + ((i * ((widthWagon*0.6) // nbButins)))) // 2

                        else:
                            xOffsetButin -= (((widthWagon*0.6) // nbButins) + ((i * ((widthWagon*0.6) // nbButins)))) // 2

                        #décalage y
                        yOffsetButin -= (heightWagon*0.005) * (i%3) #réhaussement de 1% * 0 ou 1 ou 2


                    else: #bracable == True
                        #décalage x selon le nombre de butins dans le même wagon
                        if (i % 2) == 1:
                            xOffsetButin += (((widthWagon*0.2) // nbButins) + ((i * ((widthWagon*0.2) // nbButins)))) // 2

                        else:
                            xOffsetButin -= (((widthWagon*0.2) // nbButins) + ((i * ((widthWagon*0.2) // nbButins)))) // 2

                        #décalage
                        yOffsetButin -= heightWagon*0.2 #réhaussement pour le placer sur la table
                        yOffsetButin -= (heightWagon*0.005) * (i%3) #réhaussement de 1% * 0 ou 1 ou 2


                    xImgPosition = (xButinPosition * widthWagon) + xOffsetButin

                    if yButinPosition == 'in':
                        yImgPosition = heightWagon + yOffsetButin
                    elif yButinPosition == 'out':
                        yImgPosition = yOffsetButin + (heightWagon * 0.38)
                    else:
                        print('ERROR: in colt-ze3ma.py in updateCanvasImgs: (butin, loop for other then magot, bourse)\n  the butin is in a wagon\'s list, but is own by a bandit')
                        exit()
                



                if butin.type == 'bijoux':
                    butin.img = images.createLoadedImg(widthBijoux, heightBijoux, images.imgBijoux, flip=butin.flipImg)
                elif butin.type == 'bourse':
                    butin.img = images.createLoadedImg(widthBourse, heightBourse, images.imgBourse, flip=butin.flipImg)

                img = self.playSpace.create_image(xOffsetCanvas + xImgPosition, yOffsetCanvas + yImgPosition, image=butin.img, anchor='nw')
                self.imgsOnCanvasPlaySpace.append(img)

        # FIN === ON DESSINE LES BUTINS DANS LES WAGONS ======================


        #ON DESSINE LES BANDITS ============================
        #les Offset permet de placer un personnage au centre du wagon
        xOffsetCharacter = widthWagon + (widthWagon//2) - (widthCharacter//2)
        yOffsetCharacter = (heightWagon-heightCharacter) - (heightWagon * 0.3) #hauteaur à l'intérieur du wagon


        for wagon in Game.wagons:
            nbBandits = len(wagon.bandits)

            if nbBandits == 0:
                continue

            # for i, bandit in enumerate(wagon.bandits):
            for i in range(nbBandits):
                bandit = wagon.bandits[i]

                xBanditPosition = bandit.position['x']
                yBanditPosition = bandit.position['y']
                xOffsetBandit = xOffsetCharacter
                yOffsetBandit = yOffsetCharacter

                #décalage selon le nombre de bandits dans le même wagon
                if (i % 2) == 1:
                    xOffsetBandit += ((widthWagon // nbBandits) + ((i * (widthWagon // nbBandits)))) // 4

                else:
                    xOffsetBandit -= ((widthWagon // nbBandits) + ((i * (widthWagon // nbBandits)))) // 4


                #décalage selon l'étage
                if yBanditPosition == 0: #sur le toit
                    yOffsetBandit += heightWagon*0.4
                    yOffsetBandit -= (heightWagon*0.01) * (i%3)
                if yBanditPosition == 1: #dans le wagon
                    yOffsetBandit -= (heightWagon*0.01) * (i%3) #réhaussement de 1% * 0 ou 1 ou 2


                xImgPosition = (xBanditPosition * widthWagon) + xOffsetBandit
                yImgPosition = (yBanditPosition * heightWagon) + yOffsetBandit

                bandit.img = images.createBanditPng(widthCharacter, heightCharacter, Game.COLORS[bandit.color], flip=bandit.flipImg)
                img = self.playSpace.create_image(xOffsetCanvas + xImgPosition, yOffsetCanvas + yImgPosition, image=bandit.img, anchor='nw')
                self.imgsOnCanvasPlaySpace.append(img)

        #FIN === ON DESSINE LES BANDITS ======================



        #ON DESSINE LE MARSHALL ==============================
        widthCharacter = int(widthCharacter*1.2)
        heightCharacter = int(heightCharacter*1.2)

        self.imgMarshal = images.createLoadedImg(widthCharacter,heightCharacter, images.imgMarshall)
        if self.marshallDirection == 'left':
            self.imgMarshal = images.createLoadedImg(widthCharacter,heightCharacter, images.imgMarshall, flip=True)

        for wagon in self.wagons :
            if wagon.marshall == True:
                xOffsetMarshall = widthWagon + (widthWagon//2) - (widthCharacter//2)
                yOffsetMarshall = ((heightWagon-heightCharacter) - (heightWagon * 0.3)) * 0.9 #réhaussement de 20%

                xMarshallPosition = (wagon.xPosition * widthWagon) + xOffsetMarshall
                yMarshallPosition = heightWagon + yOffsetMarshall


                img = self.playSpace.create_image(xOffsetCanvas + xMarshallPosition, yOffsetCanvas + yMarshallPosition, image=self.imgMarshal, anchor='nw')
                self.imgsOnCanvasPlaySpace.append(img)
                break
    
        # FIN === ON DESSINE LE MARSHALL ======================



        #ON DESSINE LES INVENTAIRES DES BANDITS ==============================

        for i, bandit in enumerate(self.bandits):
            self.createInventoryCanvas(bandit, widthDrawingSpace, heightCanvas, xOffsetCanvas, i)

        #FIN === ON DESSINE LES INVENTAIRES DES BANDITS ======================
    







mon_jeu = Game()

mon_jeu.mainloop()
