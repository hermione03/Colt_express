#convert color, tuple[int] as html
#ex: (252, 70, 142)  =>  #fc468e

def convertToHtml(colorTuple:tuple[int], part=0, colorHtml:str=""):
    hexaNumber = ['a', 'b', 'c', 'd', 'e', 'f']
    if part == 3:
        #colorTuple has ended been converted as colorHtml
        return '#' + colorHtml


    nbBase10:int = colorTuple[part]
    nbBase16:str = ''

    if nbBase10 == 0: #the number is "zero"
        return convertToHtml(colorTuple, part=part+1, colorHtml=colorHtml + '00')


    for _ in range (2):

        #divide the number by 16, and look at the float part
        nbBase10 /= 16
        remainder = nbBase10 - int(nbBase10)

        #multiply the float part by 16 (to find one digit)
        res = int(remainder * 16)

        if res < 10:
            nbBase16 = str(res) + nbBase16
        else:
            res -= 9
            nbBase16 = hexaNumber[res-1] + nbBase16

        nbBase10 = int(nbBase10)

    #nbBase10 has been been converted, so we proceed to the next nb of the tuple
    return convertToHtml(colorTuple, part=part+1, colorHtml=colorHtml + nbBase16)



# #test
# import random

# #convert random colors
# for _ in range(10):
#     color:tuple[int] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
#     colorHtml:str    = convertToHtml(color)
#     print(colorHtml, "<=", color)
