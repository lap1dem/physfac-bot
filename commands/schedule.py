from implib import *

import modules.keyboards as key
import modules.navigation as nav
import modules.help_functions as help

# USER COMMANDS

@bot.message_handler(commands=['schedule'])
def whats_year(message):
    nav.delete_all(message.chat.id)
    nav.del_schedule_path(message.chat.id)
    nav.update_schedule_path(message.chat.id, sch_path)
    markup_year = key.stud_years()
    markup_year.row("Вихід")
    msg = bot.send_message(
        message.chat.id,
        "Розклад занять на фізичному факультеті.\nБудь ласка, оберіть курс зі списку.",
        reply_markup=markup_year)
    bot.register_next_step_handler(msg, whats_day)


def whats_day(message):
    if message.text in c.stud_years:
        nav.update_schedule_path(
            message.chat.id,
            help.get_sch_folder(message.text)
        )
        markup_day = key.week_days()
        markup_day.row("Назад")
        msg = bot.send_message(
            message.chat.id,
            "Оберіть день.",
            reply_markup=markup_day
        )
        bot.register_next_step_handler(msg, send_schedule)
    elif message.text == "Вихід":
        key_rem = telebot.types.ReplyKeyboardRemove()
        bot.send_message(
            message.chat.id,
            "Список доступних команд:" + c.avaiable_comands,
            reply_markup=key_rem,
            parse_mode="Markdown"
        )
    else:
        msg = bot.send_message(
            message.chat.id,
            "Виберіть варіант зі списку, будь ласка!"
        )
        bot.register_next_step_handler(msg, whats_day)


def send_schedule(message):
    bot.send_chat_action(message.chat.id, 'typing')
    if message.text in c.week_days:
        key_rem = telebot.types.ReplyKeyboardRemove()
        if message.text != c.week_days[5]:
            nav.update_schedule_path(
                message.chat.id,
                help.translate_day(message.text)
            )
            schedule = open(nav.get_schedule_path(message.chat.id), 'rb')
            msg = bot.send_photo(
                message.chat.id,
                schedule,
                reply_markup=key_rem
            )
            nav.del_schedule_path(message.chat.id)
        elif message.text == c.week_days[5]:
            sch = [nav.get_schedule_path(
                message.chat.id) + '/' + x for x in help.translate_day(message.text)]
            bot.send_message(
                message.chat.id, "Розклад на тиждень:", reply_markup=key_rem)
            with open(sch[0], 'rb') as p1, open(sch[1], 'rb') as p2, open(sch[2], 'rb') as p3, open(sch[3], 'rb') as p4, open(sch[4], 'rb') as p5:
                msg = bot.send_media_group(message.chat.id,
                                           [InputMediaPhoto(p1),
                                            InputMediaPhoto(p2),
                                               InputMediaPhoto(p3),
                                               InputMediaPhoto(p4),
                                               InputMediaPhoto(p5)])
    elif message.text == "Назад":
        nav.schedule_step_back(message.chat.id)
        markup_year = key.stud_years()
        markup_year.row("Вихід")
        msg = bot.send_message(
            message.chat.id,
            "Розклад занять на фізичному факультеті.\nБудь ласка, оберіть курс зі списку.",
            reply_markup=markup_year)
        bot.register_next_step_handler(msg, whats_day)

    else:
        msg = bot.send_message(
            message.chat.id, "Виберіть варіант зі списку, будь ласка!")
        bot.register_next_step_handler(msg, send_schedule)

# ADMIN COMMANDS
