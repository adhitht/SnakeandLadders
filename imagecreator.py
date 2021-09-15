from PIL import Image

def createimage(imageloc,pos,boardloc,finallocation):
    Board = Image.open(boardloc)
    background = Board.copy()
    Image2 = Image.open(imageloc)
    foreground = Image2.copy()
    pos1 = 100-pos
    if (pos1//10)%2 != 0:
        xpos = 24+(9-(pos1%10))*96
        ypos = 40+(pos1//10)*96
    else:
        xpos = 24+(pos1%10)*96
        ypos = 40+(pos1//10)*96
    background.paste(foreground, (xpos, ypos), foreground)
    background.save(finallocation)