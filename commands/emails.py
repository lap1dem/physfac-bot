from implib import *

import modules.keyboards as key
import modules.navigation as nav
import modules.help_functions as help
import modules.data_access as data

#  USER COMMANDS

@bot.message_handler(commands=['emails'])
def whats_dep(message):
    fullname = help.get_fullname(message)
    print('"emails" command has been used by ' + fullname)
    help.log_to_dialog(message, "emails")
    nav.delete_all(message.chat.id)
    markup_dep = key.email_dep()
    markup_dep.row("Вихід")
    msg = bot.send_message(
        message.chat.id, "База імейлів викладачів.\nВиберіть кафедру або введіть прізвище.", reply_markup=markup_dep)
    bot.register_next_step_handler(msg, whats_name)


def whats_name(message):
    if message.text == "Вихід":
        key_rem = telebot.types.ReplyKeyboardRemove()
        bot.send_message(
            message.chat.id,
            "Список доступних команд:" + c.avaible_comands,
            reply_markup=key_rem,
            parse_mode="Markdown"
        )
    elif message.text in data.emails_deplist():
        nav.upd_edep(message.chat.id, message.text)
        markup_name = key.email_name(message.text)
        markup_name.row("Назад")
        msg = bot.send_message(
            message.chat.id,
            "Виберіть викладача.",
            reply_markup=markup_name
        )
        bot.register_next_step_handler(msg, get_mail)
    elif len(data.search_by_name('%{}%'.format(message.text,))) == 1:
        key_rem = telebot.types.ReplyKeyboardRemove()
        email = data.search_by_name('%{}%'.format(message.text,))
        bot.send_message(
            message.chat.id, email[0][0] + '\n' + email[0][1], reply_markup=key_rem)
    else:
        msg = bot.send_message(
            message.chat.id, "Сформулюйте запит точніше, будь ласка.")
        bot.register_next_step_handler(msg, whats_name)


def get_mail(message):
    if message.text == "Назад":
        whats_dep(message)
    elif message.text in data.emails_namelist(nav.get_edep(message.chat.id)):
        bot.send_chat_action(message.chat.id, 'typing')
        nav.upd_ename(message.chat.id, message.text)
        key_rem = telebot.types.ReplyKeyboardRemove()
        name, dep = nav.get_edata(message.chat.id)
        mail = data.get_email(name, dep)
        nav.del_edata(message.chat.id)
        bot.send_message(message.chat.id, name + " :\n" +
                         mail, reply_markup=key_rem)
    else:
        msg = bot.send_message(
            message.chat.id, "Виберіть викладача зі списку, будь ласка!")
        bot.register_next_step_handler(msg, get_mail)

# ADMIN COMMANDS

@bot.message_handler(commands=['del_email'])
def whats_dep_del(message):
    markup_dep = key.email_dep()
    msg = bot.send_message(
        message.chat.id, "Виберіть, будь ласка, кафедру.", reply_markup=markup_dep)
    bot.register_next_step_handler(msg, whats_name_del)


def whats_name_del(message):
    nav.upd_edep(message.chat.id, message.text)
    markup_name = key.email_name(message.text)
    msg = bot.send_message(
        message.chat.id, "Виберіть, будь ласка, викладача.", reply_markup=markup_name)
    bot.register_next_step_handler(msg, del_mail)


def del_mail(message):
    nav.upd_ename(message.chat.id, message.text)
    name, dep = nav.get_edata(message.chat.id)
    nav.del_edata(message.chat.id)
    data.email_remove(name, dep)
    bot.send_message(message.chat.id, "Видалено!")


@bot.message_handler(commands=['add_email'])
def add_name(message):
    msg = bot.send_message(
        message.chat.id, "Введіть, будь ласка, прізвище та ініціали.")
    bot.register_next_step_handler(msg, add_dep)


def add_dep(message):
    nav.upd_ename(message.chat.id, message.text)
    markup_dep = key.departments()
    msg = bot.send_message(
        message.chat.id, "Виберіть, будь ласка, кафедру.", reply_markup=markup_dep)
    bot.register_next_step_handler(msg, add_mail)


def add_mail(message):
    key_rem = telebot.types.ReplyKeyboardRemove()
    nav.upd_edep(message.chat.id, message.text)
    msg = bot.send_message(
        message.chat.id, "Введіть, будь ласка, пошту.", reply_markup=key_rem)
    bot.register_next_step_handler(msg, write_mail)


def write_mail(message):
    email = message.text
    name, dep = nav.get_edata(message.chat.id)
    data.add_email(name, dep, email)
    nav.del_edata(message.chat.id)
