import random
from PIL import ImageTk
from typing import Literal


#create empty class just to be able to names variables type
class Game:
    pass


class Butin():
    lootValues = {'bourse':[100,200], 'bijoux' : [500], 'magot' : [1000]}

    def __init__(self, game:Game, type:Literal['bourse', 'bijoux', 'magot'], x:int, value:int=None, position:tuple=None, bracable:bool=None):
        self.game:Game = game
        self.type:str = type
        self.value:int = random.choice(Butin.lootValues[type])
        self.position = {'x':x, 'y':'in'} #y = 'in' or 'out' or '<banditName>'
        self.bracable = True
        self.img:ImageTk.PhotoImage = None
        self.flipImg = random.choice([True, False])

        if game.LOAD_SAVE: #load from save
            self.value = value
            self.position['x'] = position[0]
            self.position['y'] = position[1]
            self.bracable = bracable

        self.game.butins.append(self)


    def __str__(self):
        return f"{self.type}({self.value}): (x={self.position['x']}, y={self.position['y']}), bracable:{self.bracable}"