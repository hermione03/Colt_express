"""
SAVE STRUCTURE :

nbPlayers, nbWagons, nbTurns, currentTurn, marshallDirection, preparation(bool), maxActions, nbButins
(wagons:)
index, type, marshall
...
(bandit:)
name, color, x, y, actions..., nbBullets
...
(butins:)
type, value, x, y, bracable
...

"""


def loadSave():
    gamedatas = []
        # 0:number of players
        # 1:number of turns
        # 2:current turn
        # 3:number of wagons
        # 4:max number of actions
        # 5:marshallDirection(str)
        # 6:preparation(bool)
        # 7:number of butins (dont return)


    wagons = []
    bandits = []
    butins = []


    #extract datas
    filePart = 1 #1=game's datas, 2=wagons, 3=bandits, 4=butins
    j = 0 #nb of line in part 2, 3 and 4
    with open('saves/save.txt', 'rt') as file:
        for line in file:
            data = ""

            if filePart == 1: #nbPlayers, nbWagons, nbTurns, currentTurn, marshallDirection, preparation, nbButins(dont return), maxActions
                for char in line:
                    if char == '\n':
                        gamedatas.append(''.join(data))
                        break
                    if char == ',':
                        gamedatas.append(''.join(data))
                        data = []
                        continue
                    data += char

                #convert data
                for i, val in enumerate(gamedatas):
                    if val == 'True':
                        val = True
                    elif val == 'False':
                        val = False

                    gamedatas[i] = val
                
                filePart += 1




            elif filePart == 2: #wagons
                datas = []
                for char in line:
                    if char == '\n':
                        datas.append(''.join(data))
                        break
                    if char == ',':
                        datas.append(''.join(data))
                        data = ""
                        continue
                    data += char
                
                wagons.append(datas)
                j += 1

                if j == int(gamedatas[3]) + 1:
                    filePart += 1
                    j = 0


            elif filePart == 3: #bandits
                datas = []
                for char in line:
                    if char == '\n':
                        datas.append(''.join(data))
                        break
                    if char == ',':
                        datas.append(''.join(data))
                        data = ""
                        continue
                    data += char
                
                bandits.append(datas)
                j += 1

                if j == int(gamedatas[0]):
                    filePart += 1
                    j = 0


            elif filePart == 4: #butins
                datas = []
                for char in line:
                    if char == '\n':
                        datas.append(''.join(data))
                        break
                    if char == ',':
                        datas.append(''.join(data))
                        data = ""
                        continue
                    data += char
                
                butins.append(datas)
                j += 1

                if j == int(gamedatas[-1]):
                    filePart += 1
                    j = 0



    #convert some data to the good type

    for wagon in wagons:
        wagon[0] = int(wagon[0])
        if wagon[2] == 'False':
            wagon[2] = False
        elif wagon[2] == 'True':
            wagon[2] = True
        else:
            wagon[2] = int(wagon[2])

    for bandit in bandits:
        bandit[2] = int(bandit[2])
        bandit[3] = int(bandit[3])
        bandit[-1] = int(bandit[-1])

    for butin in butins:
        butin[1] = int(butin[1])
        butin[2] = int(butin[2])
        if butin[4] == 'False':
            butin[4] = False
        elif butin[4] == 'True':
            butin[4] = True
        else:
            butin[4] = int(butin[4])

    


    return int(gamedatas[0]), int(gamedatas[1]), int(gamedatas[2]), int(gamedatas[3]), int(gamedatas[4]), gamedatas[5], gamedatas[6], wagons, bandits, butins






def save(nbPlayers:int, nbTurns:int, currentTurn:int, nbWagons:int, maxActions:int, marshallDirection:bool, preparationPhase:bool, wagons:list, bandits:list, butins:list):

    with open('saves/save.txt', 'w') as file:
        file.write(f'{nbPlayers},{nbTurns},{currentTurn},{nbWagons},{maxActions},{marshallDirection},{preparationPhase},{len(butins)}\n')

        for wagon in wagons:
            y = wagon.xPosition
            type = wagon.type
            marshall = wagon.marshall
            file.write(f'{y},{type},{marshall}\n')

        for bandit in bandits:
            name = bandit.name
            color = bandit.color
            x, y = bandit.position['x'], bandit.position['y']
            actions = ''
            for i, action in enumerate(bandit.actions):
                actions += action
                if i < len(bandit.actions) -1:
                    actions += ','
            bullets = bandit.bullets

            file.write(f'{name},{color},{x},{y},{actions},{bullets}\n')

        for butin in butins:
            type = butin.type
            value = butin.value
            x, y = butin.position['x'], butin.position['y']
            bracable = butin.bracable

            file.write(f'{type},{value},{x},{y},{bracable}\n')



def saveIsEmpty() -> bool:
    with open('saves/save.txt', 'rt') as file:
        for line in file:
            for char in line:
                if char == '\n':
                    return True
                else:
                    return False

    return True


def emptySave():
    with open('saves/save.txt', 'w') as file:
        file.write(f'\n')






# nbPlayers, nbTurns, currentTurn, nbWagons, nbActions, marshallDirection, preparation, wagons, bandits, butins  = loadSave()


# print('nbPlayers =', nbPlayers)
# print("nbTurns =", nbTurns)
# print("currentTurn =", currentTurn)
# print('nbWagons =', nbWagons)
# print("marshallDirection =", marshallDirection)
# print("preparation =", preparation)
# print("nbActions =", nbActions)
# print("nbButins =", len(butins))

# print('\nWagons================\n')
# for n in wagons:
#     print(n)
# print()

# print('\nBandits================\n')
# for n in bandits:
#     print(n)
# print()

# print('\nButins================\n')
# for n in butins:
#     print(n)
# print()
