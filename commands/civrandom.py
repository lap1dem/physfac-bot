from implib import *

import modules.keyboards as key
import modules.navigation as nav
import modules.help_functions as help
import modules.data_access as data
from civ_random.civrandom import *

#  USER COMMANDS

@bot.message_handler(commands=['civ'])
def civ_start(message):
    nav.delete_all(message.chat.id)
    markup_ncivs = key.civ_ncivs_key()
    markup_ncivs.row("Вихід")
    msg = bot.send_message(
        message.chat.id,
        "Рандомайзер націй в Civilization V.\nОберіть число націй на гравця.",
        reply_markup=markup_ncivs,
    )
    bot.register_next_step_handler(msg, civ_names)

def civ_names(message):
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
        key_rem = telebot.types.ReplyKeyboardRemove()
        msg = bot.send_message(
            message.chat.id,
            "Введіть імена гравців через кому.",
            reply_markup=key_rem,
        )
        bot.register_next_step_handler(msg, civ_final)

def civ_final(message):
    names = message.text
    ncivs = int(nav.civ_getncivs(message.chat.id))
    civrandom(names, ncivs)
    photos = []
    reslist = os.listdir('civ_random/results')
    reslist = [i for i in reslist if i != 'civrandom.png']
    for file in reslist:
        photos.append(
            InputMediaPhoto(
                open('civ_random/results/' + file, 'rb')
            )
        )
    bot.send_media_group(message.chat.id, photos)
    bot.send_media_group(message.chat.id, [InputMediaPhoto(
        open('civ_random/results/' + 'civrandom.png', 'rb')
    )])
