import random
import modules.tools as tools

#create empty class just to be able to names variables type
class Game:
    pass
class Bandit:
    pass
class Butin:
    pass


class Bandit():
    def __init__(self, game:Game, name:str, color:str, position:tuple=None, actions:list=None, bullets:int=None):
        self.name = name
        self.color = color
        self.colorHtml = tools.convertToHtml(game.COLORS[color])
        self.position = {'x':game.NB_WAGONS, 'y':0} #x => index du wagon dans Game.wagons, y => position dans le wagon(0=toit, 1=intérieur)
        self.actions = actions.copy() #action = 'right', 'left', 'up', 'down', 'shoot' or 'rob'
        self.game = game
        self.img = None
        self.butins = []
        self.bullets = game.MAX_BULLETS
        self.flipImg = random.choice([True, False])


        if not game.LOAD_SAVE:
            #on ajoute le bandit dans la liste bandits du bon wagon (en queue de train)
            self.game.wagons[game.NB_WAGONS].bandits.append(self)

        else: #load from save
            self.position['x'] = position[0]
            self.position['y'] = position[1]
            self.actions = actions
            self.bullets = bullets
            self.game.wagons[self.position['x']].bandits.append(self)



    def __str__(self):
        text = f"{self.name} : {self.color}, (x={self.position['x']}, y={self.position['y']})"

        for i, butin in enumerate(self.butins, start=1):
            if i == 1:
                text += '\n'
            text += f'{butin}'
            if not i == len(self.butins):
                text += '\n'

        for i, action in enumerate(self.actions, start=1):
            if i == 1:
                text += '\n'
            text += f'{action}'
            if not i == len(self.actions):
                text += ', '
        
        return text


    def formatedStr(self):
        somme = 0
        for butin in self.butins:
            somme += butin.value

        return f': {somme}$ with {len(self.butins)} butins'


    #execute the action at index 0 in self.actions
    def executeAction(self):
        if not len(self.actions):
            print("ERROR: in bandit.py in executeAction\n\tBandir has no actions")
            exit()

        if self.actions[0] in ['right', 'left', 'up', 'down']:
            self.deplacement(self.actions[0])
        elif self.actions[0] == 'shoot':
            self.shoot()
        elif self.actions[0] == 'rob':
            self.rob()

        self.actions.pop(0)



    def deplacement(self, action:str):
        xBanditPosition = self.position['x']
        yBanditPosition = self.position['y']
        banditName = self.name

        if action == 'right':
            if xBanditPosition == self.game.NB_WAGONS:
                self.game.insertTextInLog(f"{banditName} can't move {action}\n", self.colorHtml)
                return

            #on retire le bandit du wagon actuel
            for i, bandit in enumerate(self.game.wagons[xBanditPosition].bandits):
                if not bandit.name == banditName:
                    continue
                self.game.wagons[xBanditPosition].bandits.pop(i)

            #on ajoute le bandit dans le wagon destination
            self.game.wagons[xBanditPosition+1].bandits.append(self)

            self.position['x'] += 1


        if action == 'left':
            if xBanditPosition == 0:
                self.game.insertTextInLog(f"{banditName} can't move {action}\n", self.colorHtml)
                return

            #on retire le bandit du wagon actuel
            for i, bandit in enumerate(self.game.wagons[xBanditPosition].bandits):
                if not bandit.name == banditName:
                    continue
                self.game.wagons[xBanditPosition].bandits.pop(i)

            #on ajoute le bandit dans le wagon destination
            self.game.wagons[xBanditPosition-1].bandits.append(self)

            self.position['x'] -= 1


        if action == 'up':
            if yBanditPosition == 0:
                self.game.insertTextInLog(f"{banditName} can't move {action}\n", self.colorHtml)
                return
            self.position['y'] = 0

        if action == 'down':
            if yBanditPosition == 1:
                self.game.insertTextInLog(f"{banditName} can't move {action}\n", self.colorHtml)
                return
            self.position['y'] = 1

        
        self.game.insertTextInLog(f'{self.name} moves {action}\n', self.colorHtml)
        self.checkForButin()
        self.game.soundsToPlay.append('walk')




    def checkMarshallPresence(self):
        #si le bandit est sur le toit
        if self.position['y'] == 0:
            return

        #si le Marshall est dans le même wagon
        if self.game.wagons[self.position['x']].marshall == True:
            self.getHitByMarshall()



    #tire sur un Bandit, aléatoirement, à la même position
    def shoot(self):
        self.game.insertTextInLog(f'{self.name} shoot', self.colorHtml)

        if self.bullets == 0:
            self.game.insertTextInLog(f', but has no more bullets\n', self.colorHtml)
            self.game.soundsToPlay.append('magEmpty')
            return

        self.bullets -= 1
        nb_targets = 0

        #on compte le nombre de cible possible (nombre de bandit dans le même wagon ET au même étage)
        for bandit in self.game.wagons[self.position['x']].bandits:
            if bandit.name == self.name:
                continue

            if bandit.position['y'] == self.position['y']:
                nb_targets += 1

        if nb_targets == 0:
            self.game.insertTextInLog(f' on the wind\n', self.colorHtml)
            self.game.soundsToPlay.append('shootMissed')
            return


        #on tire sur un bandit
        target = None
        while(1):
            target = random.choice(self.game.wagons[self.position['x']].bandits)
            if target.name == self.name:
                continue

            if target.position['y'] == self.position['y']: #a valuable target has been found
                break


        target.getHitByBandit(self)
        self.game.soundsToPlay.append('shoot')



    #vole un butin, aléatoirement, sur sa position
    def rob(self):
        self.game.insertTextInLog(f'{self.name} rob', self.colorHtml)

        #le wagon à braquer
        wagon = self.game.wagons[self.position['x']]

        #si le wagon n'a pas de butins
        if len(wagon.butins) == 0:
            self.game.insertTextInLog(f' nothing\n', self.colorHtml)
            return
        
        #check if there is bracable butins
        butinAvailable = False

        for butin in wagon.butins:
            if butin.bracable == False:
                continue

            if self.position['y'] == 0 and butin.position['y'] == 'out':
                butinAvailable = True
            elif self.position['y'] == 1 and butin.position['y'] == 'in':
                butinAvailable = True
        
        if not butinAvailable:
            self.game.insertTextInLog(f' nothing\n', self.colorHtml)
            return
        

        #take a butin (until a good one is found)
        bracableButinFound = False

        while not bracableButinFound:
            indexButinToRob = random.randint(0, len(wagon.butins) - 1)

            if wagon.butins[indexButinToRob].bracable == True:
                if self.position['y'] == 0 and wagon.butins[indexButinToRob].position['y'] == 'out':
                    bracableButinFound = True
                elif self.position['y'] == 1 and wagon.butins[indexButinToRob].position['y'] == 'in':
                    bracableButinFound = True


        robbedButin = wagon.butins.pop(indexButinToRob)

        #add butin in bandit list
        robbedButin.bracable = False
        robbedButin.position['y'] = self.name
        self.butins.append(robbedButin)
        self.game.insertTextInLog(f' something\n', self.colorHtml)

        if robbedButin.type == 'magot':
            self.game.soundsToPlay.append('lootMagot')
        else:
            self.game.soundsToPlay.append('lootButin')




    #perd un butin, aléatoirement
    def getHitByBandit(self, ennemy:Bandit):
        self.game.insertTextInLog(f' on {self.name}\n', self.colorHtml) #couleur de l'ennemy a ajouter 


        if len(self.butins) == 0: #le bandit n'a pas de butins{self.name}
            return

        #on retire un butin du bandit, aléatoirement
        lostButin = self.butins.pop(random.randint(0, len(self.butins) - 1))

        #ennemy récupère le butin s'il n'en a pas
        if not len(ennemy.butins):
            self.game.insertTextInLog(f'{ennemy.name} steal a loot from', ennemy.colorHtml)
            self.game.insertTextInLog(f' {self.name}\n', self.colorHtml)

            lostButin.position['y'] = ennemy.name

            #on donne le butin à l'ennemi
            ennemy.butins.append(lostButin)

        
        else:
            self.game.insertTextInLog(f'{self.name} lost a loot\n', self.colorHtml)

            lostButin.position['x'] = self.position['x']
            if self.position['y'] == 0:
                lostButin.position['y'] = 'out'
            elif self.position['y'] == 1:
                lostButin.position['y'] = 'in'

            if lostButin.type == 'magot':
                lostButin.bracable = True

            #qu'on rajoute dans le wagon
            self.game.wagons[self.position['x']].butins.append(lostButin)



    #perd un butin, aléatoirement, et monte sur le toit
    def getHitByMarshall(self):
        self.game.insertTextInLog(f'{self.name} get shoot by the Marshall\n{self.name}', self.colorHtml)
        self.game.soundsToPlay.append('marshallShoot')


        if len(self.butins):
            #on retire un butin du bandit
            lostButin = self.butins.pop(random.randint(0, len(self.butins) - 1))

            lostButin.position['x'] = self.position['x']
            if self.position['y'] == 0:
                lostButin.position['y'] = 'out'
            elif self.position['y'] == 1:
                lostButin.position['y'] = 'in'

            if lostButin.type == 'magot':
                lostButin.bracable = True

            #qu'on rajoute dans le wagon
            self.game.wagons[self.position['x']].butins.append(lostButin)
            self.game.insertTextInLog(f' lost a loot and', self.colorHtml)


        #le bandit monte sur le toit
        self.position['y'] = 0
        self.game.insertTextInLog(f' flee to the roof\n', self.colorHtml)


    #called after a movement, take a random Butin on the floor (bracable == False)
    def checkForButin(self):
        wagon = self.game.wagons[self.position['x']]

        #check if there is non bracable butins
        butinAvailable = False

        for butin in wagon.butins:
            if butin.bracable == True:
                continue

            if self.position['y'] == 0 and butin.position['y'] == 'out':
                butinAvailable = True
            elif self.position['y'] == 1 and butin.position['y'] == 'in':
                butinAvailable = True
        
        if not butinAvailable:
            return
        

        #take a butin (until a good one is found)
        lootableButinFound = False

        while not lootableButinFound:
            indexButinToLoot = random.randint(0, len(wagon.butins) - 1)

            if wagon.butins[indexButinToLoot].bracable == False:
                if self.position['y'] == 0 and wagon.butins[indexButinToLoot].position['y'] == 'out':
                    lootableButinFound = True
                elif self.position['y'] == 1 and wagon.butins[indexButinToLoot].position['y'] == 'in':
                    lootableButinFound = True


        #take butin from the wagon..
        lootedButin = wagon.butins.pop(indexButinToLoot)

        lootedButin.position['y'] = self.name

        #and give it to the bandit
        self.butins.append(lootedButin)
        self.game.insertTextInLog(f'{self.name} got a loot\n', self.colorHtml)

        self.game.soundsToPlay.append('lootButin')




    def butinAtSamePosition(self, butin):
        pos:str = butin.position['y']

        if pos == 'out' and self.position['y'] == 0:
            return True
        if pos == 'int' and self.position['y'] == 1:
            return True

        return False


    def findIndexButinInGlobalList(self, butinToFind:Butin):
        for i, butin in enumerate(self.game.butins):
            if butin == butinToFind:
                return i
