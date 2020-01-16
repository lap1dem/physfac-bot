# -*- coding: utf-8 -*-
from implib import *

import modules.keyboards as key
import modules.navigation as nav
import modules.minka as minka
import modules.help_functions as help
import modules.data_access as data

from commands.schedule import *
from commands.emails import *
from commands.library import *
from commands.other import *
from commands.civrandom import *

print("Bot started")

@bot.message_handler(commands=['start'])
def start(message):

    fullname = help.get_fullname(message)
    print(fullname + ' joined!')
    username = message.from_user.username
    if username == None:
        username = '-'
    data.check_reg(message.chat.id,
                   username,
                   fullname)

    msg = """Вітаю!\nЯ - бот, написаний для студентів фізичного факультету КНУ.
    \nСписок доступних команд:""" + c.avaiable_comands + """\nКоманди також можна вибирати натиснувши кнопку |/| на панелі внизу.
    \nЯкщо бот пропонує вибір, а меню вибору не з'явилося - натисніть кнопку |88| на панелі внизу."""

    bot.send_message(
        message.chat.id,
        msg,
        parse_mode="Markdown"
    )


@bot.message_handler(commands=['about'])
def about(message):
    fullname = help.get_fullname(message)
    print('"about" command has been used by ' + fullname)
    help.log_to_dialog(message, "about")
    msg = "*Фізфак Бот v" + c.botversion + "*\n_від " + c.lastbotupdate + "_" +\
        "\n\nВи можете допомогти проекту ідеями або поповнивши базу даних" +\
        " літератури, імейлів і т.п. \n\nЗ проблемами та " +\
        "пропозиціями звертайтесь в телеграм [@vadym_bidula] або " +\
        "на [пошту](vadym.bidula@gmail.com)."

    bot.send_message(
        message.chat.id,
        msg,
        parse_mode="Markdown"
    )

bot.polling(none_stop=True)
