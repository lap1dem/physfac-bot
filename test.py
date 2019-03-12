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

@bot.message_handler(commands=['emails'])
def whats_dep(message):
    msg = bot.send_message(message.chat.id,"Введіть.")
    bot.register_next_step_handler(msg, whats_name)
def whats_name(message):
    data = database.SQL(database_name)
    a = data.search_by_name('"%{}%"'.format(message.text,))
    print(a)
    msg = bot.send_message(message.chat.id, a)

if __name__ == '__main__':
     bot.polling(none_stop = True)
