import os
from implib import *
import random
import numpy as np
from PIL import Image, ImageFont, ImageDraw
import difflib

from civ_random.balanced_random import balanced_random


dir = 'civ_random/'
W, H = (1024, 256)

font = ImageFont.truetype(dir + 'albertus-nova/Albertus Nova.otf', 92)
script_font = ImageFont.truetype(dir + 'albertus-nova/Albertus Nova Light.otf', 52)
micro_font = ImageFont.truetype(dir + 'albertus-nova/Albertus Nova Light.otf', 40)

NAMEPIC = "NAME.jpg"
iconsdir = 'icons'

def draw_name(name, queue_num = None, ban_num = None):
    NAME = Image.open(dir + NAMEPIC)
    draw = ImageDraw.Draw(NAME)
    w, h = draw.textsize(name, font=font)
    draw.text(((W - w) / 2, (H - h) / 2), name, font=font, fill='black')
    if queue_num is not None:
        draw.text((24, 24), '('+str(queue_num)+')', font=script_font, fill='black')
    if ban_num is not None:
        draw.text((24, H - 24), '['+str(ban_num)+']', font=script_font, fill='black')
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

def draw_tier(img, tier):
    draw = ImageDraw.Draw(img)
    text_tier = str(tier)
    draw.text((12, 12), text_tier, font=micro_font, fill='black')
    return img

def get_player_block(plhead, nations, tiers):
    '''
    plhead - PIL image
    nations - names of files
    '''
    imgs = [plhead]
    for nation, tier in zip(nations, tiers):
        img = Image.open(os.path.join(dir + iconsdir, nation))
        if tier is not None:
            img = draw_tier(img, tier)
        imgs.append(img)

    block = get_concat_v(imgs)
    return(block)


def remove_results():
    results = os.listdir(dir + 'results/')
    for res in results:
        os.remove(dir + 'results/' + res)


def civrandom(namelist, ncivs, bans, balanced=False, return_list=False):
    # bans - array of names without .jpg
    remove_results()

    random.shuffle(namelist)
    queue_nums = np.arange(1, len(namelist) + 1)
    random.shuffle(queue_nums)
    player_headers = []

    for name in namelist:
        qnum = random.choice(queue_nums).item()
        player_headers.append(draw_name(name, queue_num=qnum))
        queue_nums = queue_nums[queue_nums != qnum]

    if not balanced:
        iconlist = os.listdir(dir + iconsdir)
        bans = [ban + '.jpg' for ban in bans]
        to_random = [i for i in iconlist if not i in bans]
        rand_civs = [[] for i in range(len(namelist))]
        rand_tiers = [[None for j in range(ncivs)] for i in range(len(namelist))]

        for i in range(ncivs):
            for player in rand_civs:
                rand_civ = random.choice(to_random)
                to_random.remove(rand_civ)
                player.append(rand_civ)

    else:
        rand_civs, rand_tiers = balanced_random(len(namelist), ncivs, bans)

    if return_list:
        return rand_civs

    player_blocks = [get_player_block(
        player_headers[i],
        rand_civs[i],
        rand_tiers[i]
    ) for i in range(len(rand_civs))]

    # for i in range(len(player_blocks)):
    #     player_blocks[i].save(dir + "results/" + str(i) + ".png")
    final_img = get_final_image(player_blocks)
    final_img.save(dir + "results/civrandom.png")

    return None


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


def get_final_image(player_blocks):
    plen = len(player_blocks)
    phalf = int(plen/2)
    if plen > 3 and plen % 2 == 0:
        fin_im = get_concat_v([
            get_concat_h(player_blocks[:phalf]),
            get_concat_h(player_blocks[phalf:]),
        ])
    else:
        fin_im = get_concat_h(player_blocks)

    return fin_im
