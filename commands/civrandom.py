from implib import *

import modules.keyboards as key
import modules.navigation as nav
import modules.help_functions as help
import modules.data_access as data
from civ_random.civrandom import *

#  USER COMMANDS


@bot.message_handler(commands=['civ', 'цива'])
def civ_start(message):
    # if nav.check_dev_mode():
    #     send_dev_msg(message)
    #     return None

    nav.delete_all(message.chat.id)
    markup_ncivs = key.civ_ncivs_key()
    markup_ncivs.row("Вихід")
    msg = bot.send_message(
        message.chat.id,
        "Рандомайзер націй в Civilization V.\nОберіть число націй на гравця.",
        reply_markup=markup_ncivs,
    )
    bot.register_next_step_handler(msg, civ_bans)


def civ_bans(message):
    if message.text == "Вихід":
        pass

    elif message.text not in ['5', '4', '3', '2', '1']:
        markup_ncivs = key.civ_ncivs_key()
        msg = bot.send_message(
            message.chat.id,
            "Будь ласка, оберіть число зі списку.",
            reply_markup=markup_ncivs,
        )
        bot.register_next_step_handler(msg, civ_names)

    else:
        nav.civ_setncivs(message.chat.id, message.text)
        reply_markup = key.custom_key(c.civ_ban_choices)
        reply_markup.row('Вихід')
        msg = bot.send_message(
            message.chat.id,
            "Виберіть варіант банів зі списку, або введіть нації через кому українською.",
            reply_markup=reply_markup,
        )
        bot.register_next_step_handler(msg, civ_names)


def civ_names(message):
    if message.text == "Вихід":
        pass

    else:
        if message.text == "Без банів":
            bans = ''
        else:
            bans = message.text

        nav.civ_setcivbans(message.chat.id, bans)
        key_rem = telebot.types.ReplyKeyboardRemove()
        msg = bot.send_message(
            message.chat.id,
            "Введіть імена гравців через кому.",
            reply_markup=key_rem,
        )
        bot.register_next_step_handler(msg, civ_final)


def civ_final(message):
    names = message.text
    namelist = [x.strip() for x in names.split(',')]
    ncivs = int(nav.civ_getncivs(message.chat.id))
    bans = nav.civ_getcivbans(message.chat.id)
    bans = [x.strip() for x in bans.split(',')]
    bans = civ_spell_check(bans)
    bans_string = ''

    if len(namelist) * ncivs + len(bans) > 43:
        bot.send_message(
        message.chat.id,
        "У грі всього 43 нації - на всіх не вистачить.\nОберіть менше число націй на гравця.",
        )
        return None

    for b in bans:
        bans_string += b + ', '

    bans_string = bans_string[:-2]
    if bans_string == '':
        bans_string = 'Відсутні'

    bot.send_message(message.chat.id, "Забанені нації:\n" + bans_string)
    bot.send_message(message.chat.id, "Зачекайте секунду...")
    civrandom(namelist, ncivs, bans)
    photos = []
    reslist = os.listdir('civ_random/results')
    reslist = [i for i in reslist if i != 'civrandom.png']
    # for file in reslist:
    #     photos.append(
    #         InputMediaPhoto(
    #             open('civ_random/results/' + file, 'rb')
    #         )
    #     )
    # bot.send_media_group(message.chat.id, photos)
    filesize = os.stat('civ_random/results/' + 'civrandom.png').st_size / 1048576

    if filesize < 10.0:
        bot.send_photo(message.chat.id, open('civ_random/results/' + 'civrandom.png', 'rb'))
    else:
        bot.send_document(message.chat.id, open('civ_random/results/' + 'civrandom.png', 'rb'))
