#this module manage musics and sounds relative to the game
#...using pygame (pygame.mixer)

#each sounds are append in a list (exept music) to manage their volume

import pygame
from pygame import mixer as mix

import random
from typing import Literal


#audios repo
PATH_MUSICS = 'audio/musics/'
PATH_SOUNDS = 'audio/sounds/'


#musics files
MUSIC_MAIN = PATH_MUSICS + 'main-menu_valentin.wav'
MUSIC_MARIA = PATH_MUSICS + 'maria_s_rush.wav'

#sounds files
    #shoot
SOUND_SHOOT1 = PATH_SOUNDS + 'shoot/Western Outlaw Wanted Dead or Alive/REM_FIRE1.WAV'
SOUND_SHOOT2 = PATH_SOUNDS + 'shoot/Western Outlaw Wanted Dead or Alive/REM_FIRE2.WAV'
SOUND_SHOOT3 = PATH_SOUNDS + 'shoot/Western Outlaw Wanted Dead or Alive/REM_FIRE3.WAV'
SOUND_MARSHALL_SHOOT1 = PATH_SOUNDS + 'shoot/Western Outlaw Wanted Dead or Alive/COLT_FIRE1.WAV'
SOUND_MARSHALL_SHOOT2 = PATH_SOUNDS + 'shoot/Western Outlaw Wanted Dead or Alive/COLT_FIRE2.WAV'
SOUND_MARSHALL_SHOOT3 = PATH_SOUNDS + 'shoot/Western Outlaw Wanted Dead or Alive/COLT_FIRE3.WAV'
SOUND_SHOOT2 = PATH_SOUNDS + 'shoot/Western Outlaw Wanted Dead or Alive/REM_FIRE2.WAV'
SOUND_SHOOT3 = PATH_SOUNDS + 'shoot/Western Outlaw Wanted Dead or Alive/REM_FIRE3.WAV'
SOUND_SHOOTEMPTY = PATH_SOUNDS + 'shoot/Lucky Luke Western Fever/shoot_empty.wav'

    #menus
SOUND_CONFIRM = PATH_SOUNDS + 'reload/Fallout 4/Reload_MagIn_01.wav'
SOUND_CANCEL = PATH_SOUNDS + 'reload/Fallout 4/Reload_Charge_01_cropped.wav'
SOUND_NEWGAME = PATH_SOUNDS + 'reload/Fallout 4/Reload_BoltOpen_01.wav'
SOUND_LOADGAME = PATH_SOUNDS + 'reload/Fallout 4/Reload_BoltClose_01.wav'
SOUND_STARTGAME = PATH_SOUNDS + 'reload/Fallout 4/EquipUp_01.wav'
SOUND_RETURNMAINMENU1 = PATH_SOUNDS + 'bruitage/Western Outlaw Wanted Dead or Alive/STONEIMPACT1.WAV'
SOUND_RETURNMAINMENU2 = PATH_SOUNDS + 'bruitage/Western Outlaw Wanted Dead or Alive/STONEIMPACT3.WAV'
SOUND_RETURNMAINMENU3 = PATH_SOUNDS + 'bruitage/Western Outlaw Wanted Dead or Alive/STONEIMPACT4.WAV'
SOUND_LOADING = PATH_SOUNDS + 'bruitage/Western Outlaw Wanted Dead or Alive/HORSES_GALLOPING.WAV'
SOUND_RULES = PATH_SOUNDS + 'bruitage/Your Turn to Die/Book2.ogg'

    #butin
SOUND_LOOTBUTIN = PATH_SOUNDS + 'butin/Lucky Luke Western Fever/cashier.wav'
SOUND_LOOTMAGOT = PATH_SOUNDS + 'butin/Lucky Luke Western Fever/collect_hat.wav'

SOUND_STEPSIDE1 = PATH_SOUNDS + 'walk/Western Outlaw Wanted Dead or Alive/FS_WOOD1.WAV'
SOUND_STEPSIDE2 = PATH_SOUNDS + 'walk/Western Outlaw Wanted Dead or Alive/FS_WOOD2.WAV'
SOUND_STEPSIDE3 = PATH_SOUNDS + 'walk/Western Outlaw Wanted Dead or Alive/FS_WOOD3.WAV'
SOUND_STEPSIDE4 = PATH_SOUNDS + 'walk/Western Outlaw Wanted Dead or Alive/FS_WOOD4.WAV'
SOUND_STEPUPDOWN1 = PATH_SOUNDS + 'walk/Western Outlaw Wanted Dead or Alive/WLADDER1.WAV'
SOUND_STEPUPDOWN2 = PATH_SOUNDS + 'walk/Western Outlaw Wanted Dead or Alive/WLADDER2.WAV'
SOUND_STEPUPDOWN3 = PATH_SOUNDS + 'walk/Western Outlaw Wanted Dead or Alive/WLADDER3.WAV'




pygame.init()

#loads all sounds

soundShoot1 = mix.Sound(SOUND_SHOOT1) #action 'shoot'
soundShoot2 = mix.Sound(SOUND_SHOOT2) #action 'shoot'
soundShoot3 = mix.Sound(SOUND_SHOOT3) #action 'shoot'
soundShootEmpty = mix.Sound(SOUND_SHOOTEMPTY) #action 'shoot' when no ammo
soundMarshallShoot1 = mix.Sound(SOUND_MARSHALL_SHOOT1) #bandit hit by the marshall
soundMarshallShoot2 = mix.Sound(SOUND_MARSHALL_SHOOT2) #bandit hit by the marshall
soundMarshallShoot3 = mix.Sound(SOUND_MARSHALL_SHOOT3) #bandit hit by the marshall

soundConfirm = mix.Sound(SOUND_CONFIRM) #quand on appuie sur un bouton qui propose oui/non
soundCancel = mix.Sound(SOUND_CANCEL) #"no" pressed

soundNewGame = mix.Sound(SOUND_NEWGAME) #open "New" menu
soundLoadGame = mix.Sound(SOUND_LOADGAME) #open "Load" menu
soundStartGame = mix.Sound(SOUND_STARTGAME) #when the game start (after loading or create new game)
soundReturnMainMenu1 = mix.Sound(SOUND_RETURNMAINMENU1) #when return to Main Menu (from anywhere)
soundReturnMainMenu2 = mix.Sound(SOUND_RETURNMAINMENU2) #when return to Main Menu (from anywhere)
soundReturnMainMenu3 = mix.Sound(SOUND_RETURNMAINMENU3) #when return to Main Menu (from anywhere)
soundLoading = mix.Sound(SOUND_LOADING) #during loading screen at the end of the game
soundRules = mix.Sound(SOUND_RULES) #open "New" menu

soundLootButin = mix.Sound(SOUND_LOOTBUTIN) #any type of butin looted
soundLootMagot = mix.Sound(SOUND_LOOTMAGOT) #magot looted

soundStepSide1 = mix.Sound(SOUND_STEPSIDE1) #action 'move' (right, left, up, down)
soundStepSide2 = mix.Sound(SOUND_STEPSIDE2) #action 'move' (right, left, up, down)
soundStepSide3 = mix.Sound(SOUND_STEPSIDE3) #action 'move' (right, left, up, down)
soundStepSide4 = mix.Sound(SOUND_STEPSIDE4) #action 'move' (right, left, up, down)





sounds:mix.Sound = [] #used to set volume of all sounds at once
sounds.append(soundShoot1)
sounds.append(soundShoot2)
sounds.append(soundShoot3)
sounds.append(soundMarshallShoot1)
sounds.append(soundMarshallShoot2)
sounds.append(soundMarshallShoot3)
sounds.append(soundShootEmpty)
sounds.append(soundConfirm)
sounds.append(soundCancel)
sounds.append(soundNewGame)
sounds.append(soundLoadGame)
sounds.append(soundStartGame)
sounds.append(soundReturnMainMenu1)
sounds.append(soundReturnMainMenu2)
sounds.append(soundReturnMainMenu3)
sounds.append(soundLoading)
sounds.append(soundRules)
sounds.append(soundLootButin)
sounds.append(soundLootMagot)
sounds.append(soundStepSide1)
sounds.append(soundStepSide2)
sounds.append(soundStepSide3)
sounds.append(soundStepSide4)












#used at the init
def setGlobalVolume(volume:int):
    setVolume('music', volume)
    setVolume('sounds', volume)


#used when change settings in "Settings" menu change
def setVolume(type:Literal['music', 'sounds'], value:int):
    if not type in ['music', 'sounds']:
        print(f'ERROR: in audios.py, in setVolume:\n    "{type}" doesn\'t exist \n    (expected: music, sounds)')
        exit()

    if type == 'music':
        mix.music.set_volume(value/100)
    elif type == 'sounds':
        resetSoundsVolume()
        for sound in sounds:
            newVolume = sound.get_volume() * value
            sound.set_volume(newVolume/100)




#default audios volume
def resetSoundsVolume():
    soundShoot1.set_volume(1)
    soundShoot2.set_volume(1)
    soundShoot3.set_volume(1)
    soundMarshallShoot1.set_volume(1)
    soundMarshallShoot2.set_volume(1)
    soundMarshallShoot3.set_volume(1)
    soundShootEmpty.set_volume(1)
    soundConfirm.set_volume(1)
    soundCancel.set_volume(1)
    soundNewGame.set_volume(1)
    soundLoadGame.set_volume(1)
    soundStartGame.set_volume(1)
    soundReturnMainMenu1.set_volume(1)
    soundReturnMainMenu2.set_volume(1)
    soundReturnMainMenu3.set_volume(1)
    soundLoading.set_volume(1)
    soundRules.set_volume(0.5)
    soundLootButin.set_volume(1)
    soundLootMagot.set_volume(1)
    soundStepSide1.set_volume(1)
    soundStepSide2.set_volume(1)
    soundStepSide3.set_volume(1)
    soundStepSide4.set_volume(1)






#music
def playMusic(name:Literal['main', 'maria']):
    if not name in ['main', 'maria']:
        print(f'ERROR: in audios.py, in playMusic:\n    "{name}" doesn\'t exist \n    (expected: main, maria)')
        exit()

    if name == 'main':
        mix.music.load(MUSIC_MAIN)
        mix.music.play(-1)
    elif name == 'maria':
        mix.music.load(MUSIC_MARIA)
        mix.music.play(-1)


#used when loading screen starts
def fadeOutMusic(time_ms):
    mix.music.fadeout(time_ms)


#used when the player open the menu while in game
def reduceMusicVolume(volume):
    newVolume = (volume / 100) * 30 #reduction to 30% of actual value
    mix.music.set_volume(newVolume/100)

def resetMusicVolume(volume):
    mix.music.set_volume(volume/100)





#sounds
def playRandomSound():
    sound = random.choice(sounds)
    if sound == soundLoading:
        playRandomSound()
        return
    sound.play()




def playSound(name:Literal['shoot', 'marshallShoot', 'shootEmpty', 'confirm', 'cancel', 'newGame', 'loadGame', 'startGame', 'returnMainMenu', 'loading', 'rules', 'butin', 'magot', 'stepSide']):
    if not name in ['shoot', 'marshallShoot', 'shootEmpty', 'confirm', 'cancel', 'newGame', 'loadGame', 'startGame', 'returnMainMenu', 'loading', 'rules', 'butin', 'magot', 'stepSide']:
        print(f'ERROR: in audios.py, in playSound:\n    "{name}" doesn\'t exist \n    (expected: shoot, marshallShoot, shootEmpty, confirm, cancel, newGame, loadGame, startGame, returnMainMenu, loading, rules, butin, magot, stepSide)')
        exit()

    if name == 'shoot':
        choice = random.randint(1, 3)
        if choice == 1:
            soundShoot1.play()
        elif choice == 2:
            soundShoot2.play()
        elif choice == 3:
            soundShoot3.play()
    elif name == 'marshallShoot':
        choice = random.randint(1, 3)
        if choice == 1:
            soundMarshallShoot1.play()
        elif choice == 2:
            soundMarshallShoot2.play()
        elif choice == 3:
            soundMarshallShoot3.play()
    elif name == 'shootEmpty':
        soundShootEmpty.play()
    elif name == 'confirm':
        soundConfirm.play()
    elif name == 'cancel':
        soundCancel.play()
    elif name == 'newGame':
        soundNewGame.play()
    elif name == 'loadGame':
        soundLoadGame.play()
    elif name == 'startGame':
        soundStartGame.play()
    elif name == 'returnMainMenu':
        choice = random.randint(1, 3)
        if choice == 1:
            soundReturnMainMenu1.play()
        elif choice == 2:
            soundReturnMainMenu2.play()
        elif choice == 3:
            soundReturnMainMenu3.play()
    elif name == 'rules':
        soundRules.play()

    elif name == 'loading':
        soundLoading.play()
        soundLoading.fadeout(5500)
        
    elif name == 'butin':
        soundLootButin.play()
    elif name == 'magot':
        soundLootMagot.play()

    elif name == 'stepSide':
        choice = random.randint(1, 4)
        if choice == 1:
            soundStepSide1.play()
        elif choice == 2:
            soundStepSide2.play()
        elif choice == 3:
            soundStepSide3.play()
        elif choice == 4:
            soundStepSide4.play()








resetSoundsVolume()

#test
while 0:
    userInput = input("\n>")

    if userInput == 'a':
        soundShoot1.play()
    elif userInput == 'z':
        soundShoot2.play()
    elif userInput == 'e':
        soundShoot3.play()
    elif userInput == 'r':
        soundMarshallShoot1.play()
    elif userInput == 't':
        soundMarshallShoot2.play()
    elif userInput == 'y':
        soundMarshallShoot3.play()
    elif userInput == 'y':
        soundShootEmpty.play()
    elif userInput == 'u':
        soundConfirm.play()
    elif userInput == 'i':
        soundCancel.play()
    elif userInput == 'o':
        soundNewGame.play()
    elif userInput == 'p':
        soundLoadGame.play()
    elif userInput == 'q':
        soundStartGame.play()
    elif userInput == 's':
        soundReturnMainMenu1.play()
    elif userInput == 'd':
        soundReturnMainMenu2.play()
    elif userInput == 'f':
        soundReturnMainMenu3.play()
    elif userInput == 'g':
        soundLoading.play()
    elif userInput == 'h':
        soundLoading.stop()
    elif userInput == 'j':
        soundRules.play()
    elif userInput == 'k':
        soundLootButin.play()
    elif userInput == 'l':
        soundLootMagot.play()
    elif userInput == 'm':
        soundStepSide1.play()
    elif userInput == 'w':
        soundStepSide2.play()
    elif userInput == 'x':
        soundStepSide3.play()
    elif userInput == 'c':
        soundStepSide4.play()


