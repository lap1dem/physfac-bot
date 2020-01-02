from implib import *

import modules.keyboards as key
import modules.navigation as nav
import modules.help_functions as help
import modules.data_access as data

# USER COMMANDS

@bot.message_handler(commands=['library'])
def lib_start(message):
    nav.delete_all(message.chat.id)
    markup_years = key.lib_years(message.chat.id)
    markup_years.row('Вихід')
    msg = bot.send_message(
        message.chat.id,
        "Архів літератури.\nБудь ласка, оберіть розділ/файл.",
        reply_markup=markup_years
    )
    bot.register_next_step_handler(msg, lib_year)


def lib_year(message):
    if message.text == "Вихід":
        key_rem = telebot.types.ReplyKeyboardRemove()
        bot.send_message(
            message.chat.id,
            "Список доступних команд:" + c.avaiable_comands,
            reply_markup=key_rem,
            parse_mode="Markdown"
        )
    elif message.text == "Отримати літературу":
        names = nav.libGetChoosed(message.chat.id)
        key_rem = telebot.types.ReplyKeyboardRemove()
        for name in names:
            link = data.get_book(name)[0]
            bot.send_document(message.chat.id, link, reply_markup=key_rem)
    elif message.text not in [k[0] for k in data.get_lib_years()]:
        msg = bot.send_message(
            message.chat.id,
            "Оберіть варіант зі списку, будь ласка."
        )
        bot.register_next_step_handler(msg, lib_year)
    else:
        nav.libSetYear(message.chat.id, message.text)
        markup_lessons = key.lib_lessons(message.text, message.chat.id)
        markup_lessons.row('Назад')
        msg = bot.send_message(
            message.chat.id,
            "Оберіть розділ/файл.",
            reply_markup=markup_lessons
        )
        bot.register_next_step_handler(msg, lib_lesson)


def lib_lesson(message):
    if message.text == "Назад":
        markup_years = key.lib_years(message.chat.id)
        markup_years.row('Вихід')
        msg = bot.send_message(
            message.chat.id,
            "Архів літератури.\nБудь ласка, оберіть розділ/файл.",
            reply_markup=markup_years
        )
        bot.register_next_step_handler(msg, lib_year)
    elif message.text == "Отримати літературу":
        names = nav.libGetChoosed(message.chat.id)
        key_rem = telebot.types.ReplyKeyboardRemove()
        for name in names:
            link = data.get_book(name)[0]
            bot.send_document(message.chat.id, link, reply_markup=key_rem)
    elif message.text not in [k[0] for k in data.get_lib_lessons(nav.libGetYear(message.chat.id))]:
        msg = bot.send_message(
            message.chat.id,
            "Оберіть варіант зі списку, будь ласка."
        )
        bot.register_next_step_handler(msg, lib_lesson)
    else:
        nav.libSetLesson(message.chat.id, message.text)
        markup_aus = key.lib_aus(nav.libGetYear(
            message.chat.id), message.text, message.chat.id)
        markup_aus.row('Назад')
        msg = bot.send_message(
            message.chat.id,
            "Оберіть розділ/файл.",
            reply_markup=markup_aus
        )
        bot.register_next_step_handler(msg, lib_aus)


def lib_aus(message):
    if message.text == "Назад":
        markup_lessons = key.lib_lessons(
            nav.libGetYear(message.chat.id), message.chat.id)
        markup_lessons.row('Назад')
        msg = bot.send_message(
            message.chat.id,
            "Будь ласка, оберіть розділ/файл.",
            reply_markup=markup_lessons
        )
        bot.register_next_step_handler(msg, lib_lesson)
    elif message.text == "Отримати літературу":
        names = nav.libGetChoosed(message.chat.id)
        key_rem = telebot.types.ReplyKeyboardRemove()
        for name in names:
            link = data.get_book(name)[0]
            bot.send_document(message.chat.id, link, reply_markup=key_rem)
    elif message.text not in [k[0] for k in data.get_lib_aus(nav.libGetYear(message.chat.id), nav.libGetLesson(message.chat.id))[0]] + [k[0] for k in data.get_lib_aus(nav.libGetYear(message.chat.id), nav.libGetLesson(message.chat.id))[1]]:
        msg = bot.send_message(
            message.chat.id,
            "Оберіть варіант зі списку, будь ласка."
        )
        bot.register_next_step_handler(msg, lib_aus)
    else:
        if message.text in [k[0] for k in data.get_lib_aus(nav.libGetYear(message.chat.id), nav.libGetLesson(message.chat.id))[1]]:
            nav.libUpdChoosed(message.chat.id, message.text)
            markup_aus = key.lib_aus(nav.libGetYear(
                message.chat.id), nav.libGetLesson(message.chat.id), message.chat.id)
            markup_aus.row('Назад')
            msg = bot.send_message(
                message.chat.id,
                "Файл додано до списку.",
                reply_markup=markup_aus
            )
            bot.register_next_step_handler(msg, lib_aus)
        else:
            nav.libSetAus(message.chat.id, message.text)
            markup_files = key.lib_files(nav.libGetYear(message.chat.id), nav.libGetLesson(
                message.chat.id), message.text, message.chat.id)
            markup_files.row('Назад')
            msg = bot.send_message(
                message.chat.id,
                "Будь ласка, оберіть розділ/файл.",
                reply_markup=markup_files
            )
            bot.register_next_step_handler(msg, lib_finally)


def lib_finally(message):
    if message.text == "Назад":
        markup_aus = key.lib_aus(nav.libGetYear(
            message.chat.id), nav.libGetLesson(message.chat.id), message.chat.id)
        markup_aus.row('Назад')
        msg = bot.send_message(
            message.chat.id,
            "Будь ласка, оберіть розділ/файл.",
            reply_markup=markup_aus
        )
        bot.register_next_step_handler(msg, lib_aus)
    elif message.text == "Отримати літературу":
        names = nav.libGetChoosed(message.chat.id)
        key_rem = telebot.types.ReplyKeyboardRemove()
        for name in names:
            link = data.get_book(name)[0]
            bot.send_document(message.chat.id, link, reply_markup=key_rem)
    elif message.text not in [k[0] for k in data.get_lib_names(nav.libGetYear(message.chat.id), nav.libGetLesson(message.chat.id), nav.libGetAus(message.chat.id))]:
        msg = bot.send_message(
            message.chat.id,
            "Оберіть варіант зі списку, будь ласка."
        )
        bot.register_next_step_handler(msg, lib_finally)
    else:
        nav.libUpdChoosed(message.chat.id, message.text)
        markup_files = key.lib_files(nav.libGetYear(message.chat.id), nav.libGetLesson(
            message.chat.id), nav.libGetAus(message.chat.id), message.chat.id)
        markup_files.row('Назад')
        msg = bot.send_message(
            message.chat.id,
            "Файл додано до списку.",
            reply_markup=markup_files
        )
        bot.register_next_step_handler(msg, lib_finally)

# ADMIN COMMANDS

@bot.message_handler(commands=['add_books'])
def add_book(message):
    nav.delete_all(message.chat.id)
    msg = bot.send_message(message.chat.id, "Надішліть, будь ласка, файл.")
    bot.register_next_step_handler(msg, add_year)


def add_year(message):
    nav.libUpdLink(message.chat.id, message.document.file_id)
    nav.libUpdName(message.chat.id, message.document.file_name)
    markup_year = key.lib_years(message.chat.id)
    msg = bot.send_message(message.chat.id,
                           "Надішліть ще один файл або ведіть назву первинної директорії (рекомендовано назву курсу)" +
                           " або виберіть зі списку. Якщо файл відноситься до кількох курсів - " +
                           "перелічіть їх через кому (зі списку можна вибрати лише 1 варіант).",
                           reply_markup=markup_year)
    bot.register_next_step_handler(msg, add_lesson)


def add_lesson(message):
    if message.document != None:
        return add_year(message)
    else:
        nav.libSetYear(message.chat.id, message.text)
        markup_lesson = key.lib_lessons(message.text, message.chat.id)
        msg = bot.send_message(message.chat.id,
                               "Введіть вторинну директорію (рекомендовано назву предмету; * якщо відсутні).",
                               reply_markup=markup_lesson)
        bot.register_next_step_handler(msg, add_aus)


def add_aus(message):
    nav.libSetLesson(message.chat.id, message.text)
    markup_aus = key.lib_aus(nav.libGetYear(
        message.chat.id), message.text, message.chat.id)
    msg = bot.send_message(message.chat.id,
                           "Введіть імʼя автора або директорію третього рівня(* якщо відстутні).",
                           reply_markup=markup_aus)
    bot.register_next_step_handler(msg, save_to_lib)


def save_to_lib(message):
    nav.libSetAus(message.chat.id, message.text)
    key_rem = telebot.types.ReplyKeyboardRemove()
    names, links, year, lesson, aus = nav.libGetAll(message.chat.id)
    for i in range(0, len(names)):
        data.add_book(names[i], links[i], year, lesson, aus)
        bot.send_message(message.chat.id,
                         "Збережено!\n" + str(links[i]) + '\n' + str(names[i]) + '\n' + str(
                             year) + '\n' + str(lesson) + '\n' + str(aus),
                         reply_markup=key_rem)

    bot.send_message(message.chat.id,
                     "Йоу!",
                     reply_markup=key_rem)


@bot.message_handler(commands=['remove_book'])
def rb_start(message):
    nav.delete_all(message.chat.id)
    markup_years = key.lib_years(message.chat.id)
    markup_years.row('Вихід')
    msg = bot.send_message(
        message.chat.id,
        "Будь ласка, оберіть розділ/файл.",
        reply_markup=markup_years
    )
    bot.register_next_step_handler(msg, rb_year)



def rb_year(message):
    if message.text == "Вихід":
        key_rem = telebot.types.ReplyKeyboardRemove()
        bot.send_message(
            message.chat.id,
            "ок",
            reply_markup=key_rem,
            parse_mode="Markdown"
        )
    elif message.text not in [k[0] for k in data.get_lib_years()]:
        msg = bot.send_message(
            message.chat.id,
            "Оберіть варіант зі списку, будь ласка."
        )
        bot.register_next_step_handler(msg, rb_year)
    else:
        nav.libSetYear(message.chat.id, message.text)
        markup_lessons = key.lib_lessons(message.text, message.chat.id)
        markup_lessons.row('Назад')
        msg = bot.send_message(
            message.chat.id,
            "Оберіть розділ/файл.",
            reply_markup=markup_lessons
        )
        bot.register_next_step_handler(msg, rb_lesson)


def rb_lesson(message):
    if message.text == "Назад":
        markup_years = key.lib_years(message.chat.id)
        markup_years.row('Вихід')
        msg = bot.send_message(
            message.chat.id,
            "Архів літератури.\nБудь ласка, оберіть розділ/файл.",
            reply_markup=markup_years
        )
        bot.register_next_step_handler(msg, rb_year)

    elif message.text not in [k[0] for k in data.get_lib_lessons(nav.libGetYear(message.chat.id))]:
        msg = bot.send_message(
            message.chat.id,
            "Оберіть варіант зі списку, будь ласка."
        )
        bot.register_next_step_handler(msg, rb_lesson)
    else:
        nav.libSetLesson(message.chat.id, message.text)
        markup_aus = key.lib_aus(nav.libGetYear(
            message.chat.id), message.text, message.chat.id)
        markup_aus.row('Назад')
        msg = bot.send_message(
            message.chat.id,
            "Оберіть розділ/файл.",
            reply_markup=markup_aus
        )
        bot.register_next_step_handler(msg, rb_aus)


def rb_aus(message):
    if message.text == "Назад":
        markup_lessons = key.lib_lessons(
            nav.libGetYear(message.chat.id), message.chat.id)
        markup_lessons.row('Назад')
        msg = bot.send_message(
            message.chat.id,
            "Будь ласка, оберіть розділ/файл.",
            reply_markup=markup_lessons
        )
        bot.register_next_step_handler(msg, rb_lesson)
    elif message.text not in [k[0] for k in data.get_lib_aus(nav.libGetYear(message.chat.id), nav.libGetLesson(message.chat.id))[0]] + [k[0] for k in data.get_lib_aus(nav.libGetYear(message.chat.id), nav.libGetLesson(message.chat.id))[1]]:
        msg = bot.send_message(
            message.chat.id,
            "Оберіть варіант зі списку, будь ласка."
        )
        bot.register_next_step_handler(msg, rb_aus)
    else:
        if message.text in [k[0] for k in data.get_lib_aus(nav.libGetYear(message.chat.id), nav.libGetLesson(message.chat.id))[1]]:
            key_rem = telebot.types.ReplyKeyboardRemove()
            data.del_book(message.text)
            msg = bot.send_message(
                message.chat.id,
                "Файл видалено.",
                reply_markup=key_rem
            )
            nav.delete_all(message.chat.id)
        else:
            nav.libSetAus(message.chat.id, message.text)
            markup_files = key.lib_files(nav.libGetYear(message.chat.id), nav.libGetLesson(
                message.chat.id), message.text, message.chat.id)
            markup_files.row('Назад')
            msg = bot.send_message(
                message.chat.id,
                "Будь ласка, оберіть розділ/файл.",
                reply_markup=markup_files
            )
            bot.register_next_step_handler(msg, rb_finally)


def rb_finally(message):
    if message.text == "Назад":
        markup_aus = key.lib_aus(nav.libGetYear(
            message.chat.id), nav.libGetLesson(message.chat.id), message.chat.id)
        markup_aus.row('Назад')
        msg = bot.send_message(
            message.chat.id,
            "Будь ласка, оберіть розділ/файл.",
            reply_markup=markup_aus
        )
        bot.register_next_step_handler(msg, rb_aus)
    elif message.text not in [k[0] for k in data.get_lib_names(nav.libGetYear(message.chat.id), nav.libGetLesson(message.chat.id), nav.libGetAus(message.chat.id))]:
        msg = bot.send_message(
            message.chat.id,
            "Оберіть варіант зі списку, будь ласка."
        )
        bot.register_next_step_handler(msg, rb_finally)
    else:
        key_rem = telebot.types.ReplyKeyboardRemove()
        data.del_book(message.text)
        msg = bot.send_message(
            message.chat.id,
            "Файл видалено.",
            reply_markup=key_rem
        )
        nav.delete_all(message.chat.id)
