print('Started')
from config import *
import telebot
import os
import keyboards as key
import storage
import help_functions as help
import constants as c
import database
from telebot.types import InputMediaPhoto

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    msg = "Вітаю! Я - тестовий бот. Спробуй мене зламати!\nСписок доступних команд:"+c.avaible_comands
    bot.send_message(message.chat.id,msg, reply_markup = key.groups_for_year('3 курс'))

@bot.message_handler(commands=['emails'])
def whats_dep(message):
    markup_dep = key.email_dep()
    msg = bot.send_message(message.chat.id,"База імейлів викладачів.\nВиберіть кафедру або введіть прізвище.", reply_markup = markup_dep)
    bot.register_next_step_handler(msg, whats_name)
def whats_name(message):
    data = database.SQL(database_name)
    if message.text in data.emails_deplist():
        storage.upd_edep(message.chat.id, message.text)
        markup_name = key.email_name(message.text)
        msg = bot.send_message(message.chat.id,"Виберіть викладача.", reply_markup = markup_name)
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
    if message.text in data.emails_namelist(storage.get_edep(message.chat.id)):
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


@bot.message_handler(commands=['schedule'])
def whats_year(message):
    telebot.types.ReplyKeyboardRemove()
    storage.del_schedule_path(message.chat.id)
    storage.update_schedule_path(message.chat.id,'schedule')
    markup_year = key.stud_years()
    msg = bot.send_message(message.chat.id,"Розклад занять на фізичному факультеті.\nБудь ласка, оберіть курс зі списку.",reply_markup = markup_year)
    bot.register_next_step_handler(msg,whats_day)
def whats_day(message):
    if message.text in c.stud_years:
        storage.update_schedule_path(message.chat.id, help.get_sch_folder(message.text))
        markup_day = key.week_days()
        msg = bot.send_message(message.chat.id,"Оберіть день.",reply_markup=markup_day)
        bot.register_next_step_handler(msg,send_schedule)
    else:
        msg = bot.send_message(message.chat.id,"Виберіть варіант зі списку, будь ласка!")
        bot.register_next_step_handler(msg,whats_day)
def send_schedule(message):
    bot.send_chat_action(message.chat.id, 'typing')
    if message.text in c.week_days:
        key_rem = telebot.types.ReplyKeyboardRemove()
        if message.text != c.week_days[5]:
            storage.update_schedule_path(message.chat.id, help.translate_day(message.text))
            schedule = open(storage.get_schedule_path(message.chat.id), 'rb')
            msg = bot.send_photo(message.chat.id, schedule, reply_markup = key_rem)
            storage.del_schedule_path(message.chat.id)
        #     # !!!!!!!!!!!!!!!!!!!!!!!!!!!
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

    else:
        msg = bot.send_message(message.chat.id,"Виберіть варіант зі списку, будь ласка!")
        bot.register_next_step_handler(msg,send_schedule)



if __name__ == '__main__':
     bot.polling(none_stop = True)
