# %%
from tkinter import *
import os
import random
import pyscreenshot as ImageGrab
import time

dir_path = os.path.dirname(os.path.realpath(__file__))
icons_path = os.path.join(os.path.join(dir_path,'icons'),'civs')
icons = os.listdir(icons_path)
icons.sort()

names = "Вова, Вадим, Лада"
ncivs = 4

def civ_random():
    root = Tk()
    namelist = [x.strip() for x in names.split(',')]
    nplayers = len(namelist)


    # if type(ncivs) != 'int' or ncivs < 1 or ncivs > 6:
    #     return(None)
    # if nplayers == 0:
    #     return(None)

    bans = ['Вавилон', 'Гуни', 'Іспанія', 'Венеція',]
    ficons = [i for i in icons if i[:-4] not in bans]
    civimages = [PhotoImage(file=os.path.join(icons_path,i)) for i in ficons]
    civnames = [i[:-4] for i in ficons]
    applied_civs = [civnames[i] for i in range(len(civnames)) if civnames[i] not in bans]
    civnum = ncivs * nplayers
    rand_civs = list()
    for i in range(civnum):
        rand_civ = random.choice(applied_civs)
        applied_civs.remove(rand_civ)
        rand_civs.append(rand_civ)

    can = Canvas(root)
    frame = Frame(can)
    can.pack()
    frame.pack()
    imgs = [PhotoImage(file=os.path.join(icons_path,i+'.png')) for i in rand_civs]

    labelFrames = [LabelFrame(frame, text=name, font=12) for name in namelist]
    labels = list()
    for i in range(len(labelFrames)):
        lf = labelFrames[i]
        for j in range(ncivs):
            labels.append(
                Label(
                    lf,
                    text = rand_civs[ncivs*i + j],
                    image = imgs[ncivs*i + j],
                    compound='left',
            ))

    for i in range(len(labels)):
        labels[i].image = imgs[i]
        labels[i].pack()

    for i in range(int(len(labelFrames)/2)+1):
        for j in range(4):
            try:
                labelFrames[4*i+j].grid(row=i, column=j)
            except IndexError:
                pass

    can.update()
    x = root.winfo_x()
    y = root.winfo_y()
    width = root.winfo_width()
    height = root.winfo_height()

    time.sleep(1)
    im = ImageGrab.grab(bbox=(x, y, x + width, y + height))
    im.save("civ.png")
    root.destroy()
