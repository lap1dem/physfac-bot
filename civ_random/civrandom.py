import os
from implib import *
import random
import numpy as np
from PIL import Image, ImageFont, ImageDraw
import difflib


dir = 'civ_random/'
# W, H = (256, 64)
W, H = (1024, 256)

font = ImageFont.truetype(dir + 'albertus-nova/Albertus Nova.otf', 92)

NAMEname = "NAME2.jpg"
iconsdir = 'icons2'

def draw_name(name):
    NAME = Image.open(dir + NAMEname)
    draw = ImageDraw.Draw(NAME)
    w, h = draw.textsize(name, font=font)
    draw.text(((W - w) / 2, (H - h) / 2), name, font=font, fill="black")
    return(NAME)


def get_concat_h(images):
    widths = [im.width for im in images]
    heights = [im.height for im in images]
    tot_width = np.sum(widths)
    tot_height = np.max(heights)
    res = Image.new('RGB', (tot_width, tot_height))
    cur_width = 0

    for img in images:
        res.paste(
            img,
            (cur_width, 0),
        )
        cur_width += img.width

    return res


def get_concat_v(images):
    widths = [im.width for im in images]
    heights = [im.height for im in images]
    tot_width = np.max(widths)
    tot_height = np.sum(heights)
    res = Image.new('RGB', (tot_width, tot_height))
    cur_height = 0

    for img in images:
        res.paste(
            img,
            (0, cur_height),
        )
        cur_height += img.height

    return res


def get_player_block(plhead, nations):
    '''
    plhead - PIL image
    nations - names of files
    '''
    imgs = [plhead]
    for nation in nations:
        img = Image.open(os.path.join(dir + iconsdir, nation))
        imgs.append(img)

    block = get_concat_v(imgs)
    return(block)


def remove_results():
    results = os.listdir(dir + 'results/')
    for res in results:
        os.remove(dir + 'results/' + res)


def civrandom(names, ncivs, bans):
    # bans - array of names without .jpg
    remove_results()

    bans = [ban + '.jpg' for ban in bans]
    iconlist = os.listdir(dir + iconsdir)
    # bans = [
    #     'Іспанія.jpg',
    #     'Вавилон.jpg',
    #     'Гуни.jpg',
    #     'Венеція.jpg',
    # ]

    to_random = [i for i in iconlist if not i in bans]

    namelist = [x.strip() for x in names.split(',')]
    random.shuffle(namelist)

    player_headers = [draw_name(name) for name in namelist]

    rand_civs = [[] for i in range(len(namelist))]

    for i in range(ncivs):
        for player in rand_civs:
            rand_civ = random.choice(to_random)
            to_random.remove(rand_civ)
            player.append(rand_civ)

    player_blocks = [get_player_block(
        player_headers[i],
        rand_civs[i],
    ) for i in range(len(rand_civs))]

    for i in range(len(player_blocks)):
        player_blocks[i].save(dir + "results/" + str(i) + ".png")
    final_img = get_concat_h(player_blocks)
    final_img.save(dir + "results/civrandom.png")


def civ_spell_check(words):
    # words - array of strings
    from civ_random.civ_dict import civ_dict
    corr_words = []

    for word in words:
        word_list = difflib.get_close_matches(word, civ_dict, n=1)

        if len(word_list) != 0:
            corr_words.append(word_list[0].capitalize())
        else:
            pass

    return(corr_words)
