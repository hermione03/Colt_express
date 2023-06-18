from PIL import ImageTk, Image



imgIcon = Image.open('png/windowIcon_train.ico')

imgPaysage = Image.open("png/landscape.png")
imgPaysageSafeHeight = Image.open("png/landscapeSafeHeight.png")

imgRight = Image.open('png/menuSpace_button_arrow_right.png')
imgLeft = Image.open('png/menuSpace_button_arrow_left.png')
imgUp = Image.open('png/menuSpace_button_arrow_up.png')
imgDown = Image.open('png/menuSpace_button_arrow_down.png')
imgShoot = Image.open('png/menuSpace_button_shoot.png')
imgRob = Image.open('png/menuSpace_button_rob.png')

imgLoco = Image.open('png/loco_v2.png') #width = 200%
imgWagon = Image.open('png/wagon_v2.png')
imgQueue = Image.open('png/queue_v2.png')

imgBourse = Image.open("png/bourse_v2.png") #width = 13%, height = 11%
imgBijoux = Image.open("png/bijoux_v1.png") #width = 7%, height = 6%
imgMagot = Image.open("png/magot_v1.png") #width = 35%, height = 20%

imgMarshall = Image.open('png/marshall_v1.png') #width = 26%, height = 42%

imgBody = Image.open("png/bandit_body_v1.png") #width = 26%, height = 42%
imgDetails = Image.open("png/bandit_details_v1.png") #width = 26%, height = 42%

imgIconMinution = Image.open("png/icone_munition_v1.png")
imgIconBourse = Image.open("png/icone_bourse_v1.png")
imgIconBanditBody = Image.open("png/icone_bandit_body_v1.png")
imgIconBanditDetails = Image.open("png/icone_bandit_details_v1.png")





def createLoadedImg(width:int, height:int, loadedImg:Image, flip:bool=False):
    if flip:
        loadedImg = loadedImg.transpose(Image.FLIP_LEFT_RIGHT)

    loadedImg = loadedImg.resize((width, height))
    return ImageTk.PhotoImage(loadedImg)


def createBanditPng(width:int, height:int, color:tuple[int], justHead:bool=False, flip:bool=False):
    body = None
    details = None

    if justHead:
        body = imgIconBanditBody
        details = imgIconBanditDetails
        body = body.resize((width, height), Image.NEAREST)
        details = details.resize((width, height), Image.NEAREST)
    else:
        body = imgBody
        details = imgDetails
        body = body.resize((width, height))
        details = details.resize((width, height))
    
    if flip:
        body = body.transpose(Image.FLIP_LEFT_RIGHT)
        details = details.transpose(Image.FLIP_LEFT_RIGHT)



    #on modifie la couleur de chaque pixel du png 
    for y in range(details.height):
        for x in range(details.width):
            if details.getpixel((x, y)) != (0, 0, 0, 0): #est un pixel transparent
                tempColor = (color[0], color[1], color[2], details.getpixel((x, y))[3])
                details.putpixel((x, y), value=tempColor)

    img = Image.alpha_composite(body, details)
    return ImageTk.PhotoImage(img)