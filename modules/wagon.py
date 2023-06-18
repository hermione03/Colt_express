import random
from typing import Literal
from modules.butin import Butin


#create empty class just to be able to names variables type
class Game:
    pass
class Bandit:
    pass



class Wagon():
    butinTypes = ['bourse', 'bijoux'] #'magot' only apply for type == 'loco'


    def __init__(self, game:Game, x:int, type:Literal['loco', 'wagon', 'queue'], marshall:bool=None):
        self.xPosition = x
        self.marshall = False
        self.type = type #'loco' ou 'wagon' or 'queue'
        self.bandits:list[Bandit] = []
        self.butins:list[Butin] = []


        if game.LOAD_SAVE: #load from a save
            self.marshall = marshall

        else:
            #replissage de butins, en fonction de type
            if self.type == 'loco':
                self.butins.append(Butin(game, 'magot', self.xPosition))

            elif self.type == 'wagon':
                for _ in range(random.randint(game.MIN_BUTINS, game.MAX_BUTINS)):
                    self.butins.append(Butin(game, random.choice(Wagon.butinTypes), self.xPosition))



    def __str__(self):
        text = f"{self.type}(x={self.xPosition}) marshall:{self.marshall}"

        for i, butin in enumerate(self.butins, start=1):
            if i == 1:
                text += '\n'
            text += f"{butin}"
            if not i == len(self.butins):
                text += '\n'

        for i, bandit in enumerate(self.bandits, start=1):
            if i == 1:
                text += '\n'
            text += f"{bandit}"
            if not i == len(self.bandits):
                text += '\n'
        
        text += '\n'

        
        return text

