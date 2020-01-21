from implib import *

import modules.keyboards as key
import modules.navigation as nav
import modules.help_functions as help
import modules.data_access as data

@bot.message_handler(commands=['textschedule'])
def choosefunc(message):
#     if nav.check_dev_mode():
#         send_dev_msg(message)
#         return None

    nav.delete_all(message.chat.id)
    # markup = key.custom_key(c.sch_plus_funcs)
    # markup.row('Вихід')
    markup = key.sch_plus_years()
    markup.row('Назад')
    msg = bot.send_message(
        message.chat.id,
        # "Розширені можливості для розкладу.\nБудь ласка, оберіть функцію зі списку.",
        "Розклад у текстовому форматі.\nОберіть курс.",
        reply_markup=markup)

    # bot.register_next_step_handler(msg, go_to_func)
    bot.register_next_step_handler(msg, choose_group)

def go_to_func(message):
    if message.text == 'Вихід':
        key_rem = telebot.types.ReplyKeyboardRemove()
        bot.send_message(
            message.chat.id,
            "Список доступних команд:" + c.avaiable_comands,
            reply_markup=key_rem,
            parse_mode="Markdown"
        )

    elif message.text not in c.sch_plus_funcs:
        markup = key.custom_key(c.sch_plus_funcs)
        markup.row('Вихід')
        msg = bot.send_message(
            message.chat.id,
            "Будь ласка, оберіть функцію зі списку.",
            reply_markup=markup)

        bot.register_next_step_handler(msg, go_to_func)

    elif message.text == 'Розклад':
        markup = key.sch_plus_years()
        markup.row('Назад')
        msg = bot.send_message(
            message.chat.id,
            "Оберіть курс.",
            reply_markup=markup)

        bot.register_next_step_handler(msg, choose_group)

# 'Розклад' case
def choose_group(message):
    if message.text == 'Назад':
        markup = key.custom_key(c.sch_plus_funcs)
        markup.row('Вихід')
        msg = bot.send_message(
            message.chat.id,
            "Будь ласка, оберіть функцію зі списку.",
            reply_markup=markup)

        bot.register_next_step_handler(msg, go_to_func)

    elif message.text in data.sch_get_years():
        nav.sch_set_year(message.chat.id, message.text)
        markup = key.sch_plus_groups(message.chat.id)
        markup.row('Назад')
        msg = bot.send_message(
            message.chat.id,
            "Оберіть групу.",
            reply_markup=markup)

        bot.register_next_step_handler(msg, choose_day)

    else:
        markup = key.sch_plus_years()
        markup.row('Назад')
        msg = bot.send_message(
            message.chat.id,
            "Будь ласка, оберіть курс зі списку.",
            reply_markup=markup)

        bot.register_next_step_handler(msg, choose_group)

def choose_day(message):
    if message.text == 'Назад':
        markup = key.sch_plus_years()
        markup.row('Назад')
        msg = bot.send_message(
            message.chat.id,
            "Оберіть курс.",
            reply_markup=markup)

        bot.register_next_step_handler(msg, choose_group)

    elif message.text in data.sch_get_groups(nav.sch_get_year(message.chat.id)):
        nav.sch_set_group(message.chat.id, message.text)
        markup = key.sch_plus_days(message.chat.id)
        markup.row('Тиждень')
        markup.row('Назад')
        msg = bot.send_message(
            message.chat.id,
            "Оберіть день.",
            reply_markup=markup)

        bot.register_next_step_handler(msg, send_text_schedule)

    else:
        markup = key.sch_plus_groups(message.chat.id)
        markup.row('Назад')
        msg = bot.send_message(
            message.chat.id,
            "Будь ласка, оберіть групу і списку.",
            reply_markup=markup)

        bot.register_next_step_handler(msg, choose_day)

def send_text_schedule(message):
    if message.text == 'Назад':
        markup = key.sch_plus_groups(message.chat.id)
        markup.row('Назад')
        msg = bot.send_message(
            message.chat.id,
            "Оберіть групу зі списку.",
            reply_markup=markup)
        bot.register_next_step_handler(msg, choose_day)

    elif message.text in data.sch_get_days(nav.sch_get_year(message.chat.id), nav.sch_get_group(message.chat.id)):
        year = nav.sch_get_year(message.chat.id)
        group = nav.sch_get_group(message.chat.id)
        day = message.text
        lessons = data.sch_get_lessons(year, group, day)
        msg = help.create_sch_message(lessons)
        key_rem = telebot.types.ReplyKeyboardRemove()
        bot.send_message(
            message.chat.id,
            msg,
            reply_markup=key_rem,
            parse_mode="Markdown"
        )

    elif message.text == 'Тиждень':
        year = nav.sch_get_year(message.chat.id)
        group = nav.sch_get_group(message.chat.id)
        days = data.sch_get_days(year, group)
        for day in days:
            lessons = data.sch_get_lessons(year, group, day)
            msg = help.create_sch_message(lessons)
            key_rem = telebot.types.ReplyKeyboardRemove()
            bot.send_message(
                message.chat.id,
                msg,
                reply_markup=key_rem,
                parse_mode="Markdown"
            )

    else:
        markup = key.sch_plus_days(message.chat.id)
        markup.row('Назад')
        msg = bot.send_message(
            message.chat.id,
            "Оберіть день зі списку.",
            reply_markup=markup)

        bot.register_next_step_handler(msg, send_text_schedule)


