# -*- coding: utf-8 -*-

from config import *
import telebot
import os
import keyboards as key
import storage
import help_functions as help
import constants as c
import database
import json
from telebot.types import InputMediaPhoto

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['test'])
def test(message):
    storage.delete_all(message.chat.id)

@bot.message_handler(commands=['start'])
def start(message):
    msg = """Вітаю!\nЯ - бот, написаний для студентів фізичного факультету КНУ.
    \nСписок доступних команд:"""+c.avaible_comands+"""\nКоманди також можна вибирати натиснувши кнопку |/| на панелі внизу."""
    bot.send_message(
        message.chat.id,
        msg,
        parse_mode = "Markdown"
    )
    data = database.SQL(database_name)
    data.add_user(message.chat.id)

@bot.message_handler(commands=['about'])
def about(message):
    msg = "*Фізфак Бот v0.6.3*\n_від 16.05.2019_"+\
        "\n\nВи можете допомогти проекту ідеями або поповнивши базу даних"+\
        " літератури, імейлів і т.п. \n\nЗ проблемами та "+\
        "пропозиціями звертайтесь в телеграм [@vadym_bidula] або "+\
        "на [пошту](vadym.bidula@gmail.com)."

    bot.send_message(
        message.chat.id,
        msg,
        parse_mode = "Markdown"
    )

@bot.message_handler(commands=['emails'])
def whats_dep(message):
    storage.delete_all(message.chat.id)
    markup_dep = key.email_dep()
    markup_dep.row("Вихід")
    msg = bot.send_message(message.chat.id,"База імейлів викладачів.\nВиберіть кафедру або введіть прізвище.", reply_markup = markup_dep)
    bot.register_next_step_handler(msg, whats_name)

def whats_name(message):
    data = database.SQL(database_name)
    if message.text == "Вихід":
        key_rem = telebot.types.ReplyKeyboardRemove()
        bot.send_message(
            message.chat.id,
            "Список доступних команд:"+c.avaible_comands,
            reply_markup=key_rem,
            parse_mode = "Markdown"
            )
    elif message.text in data.emails_deplist():
        storage.upd_edep(message.chat.id, message.text)
        markup_name = key.email_name(message.text)
        markup_name.row("Назад")
        msg = bot.send_message(
            message.chat.id,
            "Виберіть викладача.",
            reply_markup = markup_name
            )
        bot.register_next_step_handler(msg, get_mail)
    elif len(data.search_by_name('"%{}%"'.format(message.text,))) == 1:
        key_rem = telebot.types.ReplyKeyboardRemove()
        email = data.search_by_name('"%{}%"'.format(message.text,))
        bot.send_message(message.chat.id, email[0][0] +'\n'+ email[0][1], reply_markup = key_rem)
    else:
        msg = bot.send_message(message.chat.id,"Сформулюйте запит точніше, будь ласка.")
        bot.register_next_step_handler(msg, whats_name)

def get_mail(message):
    data = database.SQL(database_name)
    if message.text == "Назад":
        whats_dep(message)
    elif message.text in data.emails_namelist(storage.get_edep(message.chat.id)):
        bot.send_chat_action(message.chat.id, 'typing')
        storage.upd_ename(message.chat.id, message.text)
        key_rem = telebot.types.ReplyKeyboardRemove()
        name, dep = storage.get_edata(message.chat.id)
        mail = data.get_email(name, dep)
        storage.del_edata(message.chat.id)
        bot.send_message(message.chat.id,name + " :\n" + mail, reply_markup = key_rem)
    else:
        msg = bot.send_message(message.chat.id,"Виберіть викладача зі списку, будь ласка!")
        bot.register_next_step_handler(msg, get_mail)


@bot.message_handler(commands=['del_email'])
def whats_dep_del(message):
    markup_dep = key.email_dep()
    msg = bot.send_message(message.chat.id,"Виберіть, будь ласка, кафедру.", reply_markup = markup_dep)
    bot.register_next_step_handler(msg, whats_name_del)

def whats_name_del(message):
    storage.upd_edep(message.chat.id, message.text)
    markup_name = key.email_name(message.text)
    msg = bot.send_message(message.chat.id,"Виберіть, будь ласка, викладача.", reply_markup = markup_name)
    bot.register_next_step_handler(msg, del_mail)

def del_mail(message):
    storage.upd_ename(message.chat.id, message.text)
    name, dep = storage.get_edata(message.chat.id)
    storage.del_edata(message.chat.id)
    data = database.SQL(database_name)
    data.email_remove(name, dep)
    bot.send_message(message.chat.id,"Видалено!")


@bot.message_handler(commands=['add_email'])
def add_name(message):
    msg = bot.send_message(message.chat.id,"Введіть, будь ласка, прізвище та ініціали.")
    bot.register_next_step_handler(msg, add_dep)

def add_dep(message):
    storage.upd_ename(message.chat.id, message.text)
    markup_dep = key.departments()
    msg = bot.send_message(message.chat.id,"Виберіть, будь ласка, кафедру.", reply_markup = markup_dep)
    bot.register_next_step_handler(msg, add_mail)

def add_mail(message):
    key_rem = telebot.types.ReplyKeyboardRemove()
    storage.upd_edep(message.chat.id, message.text)
    msg = bot.send_message(message.chat.id,"Введіть, будь ласка, пошту.",reply_markup = key_rem)
    bot.register_next_step_handler(msg, write_mail)

def write_mail(message):
    email = message.text
    name, dep = storage.get_edata(message.chat.id)
    data = database.SQL(database_name)
    data.add_email(name, dep, email)
    storage.del_edata(message.chat.id)

@bot.message_handler(commands=['howmany'])
def howmany(message):
    data = database.SQL(database_name)
    n = data.count_rows('users')
    data.close()
    bot.send_message(message.chat.id, "З ботом контактували "+str(n)+" юзерів.")

@bot.message_handler(commands=['add_books'])
def add_book(message):
    storage.delete_all(message.chat.id)
    msg = bot.send_message(message.chat.id,"Надішліть, будь ласка, файл.")
    bot.register_next_step_handler(msg, add_year)

def add_year(message):
    storage.libUpdLink(message.chat.id,message.document.file_id)
    storage.libUpdName(message.chat.id,message.document.file_name)
    markup_year = key.lib_years()
    msg = bot.send_message(message.chat.id,
        "Надішліть ще один файл або ведіть назву первинної директорії (рекомендовано назву курсу)"+\
        " або виберіть зі списку. Якщо файл відноситься до кількох курсів - "+\
        "перелічіть їх через кому (зі списку можна вибрати лише 1 варіант).",
            reply_markup = markup_year)
    bot.register_next_step_handler(msg, add_lesson)

def add_lesson(message):
    if message.document != None:
        return add_year(message)
    else:
        storage.libSetYear(message.chat.id,message.text)
        markup_lesson = key.lib_lessons(message.text)
        msg = bot.send_message(message.chat.id,
        "Введіть вторинну директорію (рекомендовано назву предмету; * якщо відсутні).",
        reply_markup = markup_lesson)
        bot.register_next_step_handler(msg, add_aus)

def add_aus(message):
    storage.libSetLesson(message.chat.id,message.text)
    markup_aus = key.lib_aus(storage.libGetYear(message.chat.id), message.text)
    msg = bot.send_message(message.chat.id,
    "Введіть імʼя автора або директорію третього рівня(* якщо відстутні).",
    reply_markup = markup_aus)
    bot.register_next_step_handler(msg, save_to_lib)

def save_to_lib(message):
    storage.libSetAus(message.chat.id,message.text)
    key_rem = telebot.types.ReplyKeyboardRemove()
    names, links, year, lesson, aus = storage.libGetAll(message.chat.id)
    data = database.SQL(database_name)
    for i in range(0, len(names)):
        data.add_book(names[i], links[i], year, lesson, aus)
    data.close()
    bot.send_message(message.chat.id,
    "Збережено!",
    reply_markup = key_rem)

@bot.message_handler(commands=['schedule'])
def whats_year(message):
    storage.delete_all(message.chat.id)
    storage.del_schedule_path(message.chat.id)
    storage.update_schedule_path(message.chat.id,'schedule')
    markup_year = key.stud_years()
    markup_year.row("Вихід")
    msg = bot.send_message(
        message.chat.id,
        "Розклад занять на фізичному факультеті.\nБудь ласка, оберіть курс зі списку.",
        reply_markup = markup_year)
    bot.register_next_step_handler(msg,whats_day)

def whats_day(message):
    if message.text in c.stud_years:
        storage.update_schedule_path(
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
        bot.register_next_step_handler(msg,send_schedule)
    elif message.text == "Вихід":
        key_rem = telebot.types.ReplyKeyboardRemove()
        bot.send_message(
            message.chat.id,
            "Список доступних команд:"+c.avaible_comands,
            reply_markup=key_rem,
            parse_mode = "Markdown"
            )
    else:
        msg = bot.send_message(
            message.chat.id,
            "Виберіть варіант зі списку, будь ласка!"
            )
        bot.register_next_step_handler(msg,whats_day)

def send_schedule(message):
    bot.send_chat_action(message.chat.id, 'typing')
    if message.text in c.week_days:
        key_rem = telebot.types.ReplyKeyboardRemove()
        if message.text != c.week_days[5]:
            storage.update_schedule_path(
                message.chat.id,
                help.translate_day(message.text)
                )
            schedule = open(storage.get_schedule_path(message.chat.id), 'rb')
            msg = bot.send_photo(
                message.chat.id,
                schedule,
                reply_markup = key_rem
                )
            storage.del_schedule_path(message.chat.id)
        elif message.text == c.week_days[5]:
            sch = [storage.get_schedule_path(message.chat.id) + '/' + x for x in help.translate_day(message.text)]
            bot.send_message(message.chat.id, "Розклад на тиждень:", reply_markup = key_rem)
            with open(sch[0], 'rb') as p1 , open(sch[1], 'rb') as p2, open(sch[2], 'rb') as p3, open(sch[3], 'rb') as p4, open(sch[4], 'rb') as p5:
                msg = bot.send_media_group(message.chat.id,
                [InputMediaPhoto(p1),
                InputMediaPhoto(p2),
                InputMediaPhoto(p3),
                InputMediaPhoto(p4),
                InputMediaPhoto(p5)])
    elif message.text == "Назад":
        storage.schedule_step_back(message.chat.id)
        markup_year = key.stud_years()
        markup_year.row("Вихід")
        msg = bot.send_message(
            message.chat.id,
            "Розклад занять на фізичному факультеті.\nБудь ласка, оберіть курс зі списку.",
            reply_markup = markup_year)
        bot.register_next_step_handler(msg,whats_day)

    else:
        msg = bot.send_message(message.chat.id,"Виберіть варіант зі списку, будь ласка!")
        bot.register_next_step_handler(msg,send_schedule)


@bot.message_handler(commands=['library'])
def lib_start(message):
    bot.send_message(message.chat.id,
        "Усе майже готово. Бібліотека відкриється найближчим часом(після сесії).")
    # storage.delete_all(message.chat.id)
    # storage.del_lib_path(message.chat.id)
    # storage.update_lib_path(message.chat.id,'library')
    # markup_lib = key.library_list(storage.get_lib_path(message.chat.id))
    # markup_lib.row("Вихід")
    # msg = bot.send_message(
    #     message.chat.id,
    #     "Архів літератури.\nБудь ласка, оберіть розділ/файл.",
    #     reply_markup = markup_lib
    #     )
    # bot.register_next_step_handler(msg, lib_next_step)

# def lib_next_step(message):
    # if message.text == "Вихід":
    #             key_rem = telebot.types.ReplyKeyboardRemove()
    #             bot.send_message(
    #                 message.chat.id,
    #                 "Список доступних команд:"+c.avaible_comands,
    #                 reply_markup=key_rem,
    #                 parse_mode = "Markdown"
    #                 )
    # elif message.text == "Назад":
    #     storage.lib_step_back(message.chat.id)
    #     markup_lib = key.library_list(storage.get_lib_path(message.chat.id))
    #     if storage.lib_at_start(message.chat.id):
    #         markup_lib.row("Вихід")
    #     else:
    #         markup_lib.row("Назад")
    #     msg = bot.send_message(message.chat.id,"Oберіть розділ/файл.",reply_markup = markup_lib)
    #     bot.register_next_step_handler(msg, lib_next_step)
    #
    # elif os.path.exists(storage.get_lib_path(message.chat.id) + '/' + message.text):
    #     storage.update_lib_path(message.chat.id,message.text)
    #     if os.path.isfile(storage.get_lib_path(message.chat.id)):
    #         key_rem = telebot.types.ReplyKeyboardRemove()
    #         data = database.SQL(database_name)
    #
    #         if not data.sent_files_check(storage.get_lib_path(message.chat.id)):
    #             file = open(storage.get_lib_path(message.chat.id), 'rb')
    #             bot.send_message(message.chat.id, "Зачекайте, будь ласка.\nФайл надсилається.")
    #             bot.send_chat_action(message.chat.id, 'upload_document')
    #             msg = bot.send_document(message.chat.id, file, reply_markup = key_rem)
    #             data.sent_files_add(storage.get_lib_path(message.chat.id), msg.document.file_id)
    #         else:
    #             file = data.sent_files_get_id(storage.get_lib_path(message.chat.id))
    #             bot.send_chat_action(message.chat.id, 'upload_document')
    #             msg = bot.send_document(message.chat.id, file, reply_markup = key_rem)
    #
    #     else:
    #         markup_lib = key.library_list(storage.get_lib_path(message.chat.id))
    #         markup_lib.row("Назад")
    #         msg = bot.send_message(
    #             message.chat.id,
    #             "Oберіть розділ/файл.",
    #             reply_markup = markup_lib
    #             )
    #         bot.register_next_step_handler(msg, lib_next_step)
    # else:
    #     markup_lib = key.library_list(storage.get_lib_path(message.chat.id))
    #     msg = bot.send_message(
    #         message.chat.id,
    #         "Будь ласка, оберіть розділ/файл зі списку.",
    #         reply_markup = markup_lib
    #         )
    #     bot.register_next_step_handler(msg, lib_next_step)




if __name__ == '__main__':
     bot.polling(none_stop = True)
