from telebot.types import (
    ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
)
from config import *
import constants
import modules.psql_tools as data
import os
import modules.storage as storage

work_dir = os.getcwd()

def stud_years():
    # Список курсів
    key = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
    key.row('1 курс','2 курс')
    key.row('3 курс','4 курс')
    key.row(' 1 курс м.','2 курс м.')
    # key.row('Вихід')
    return key

def week_days():
    # Список робочих днів
    key = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
    key.row('Понеділок','Вівторок','Середа',)
    key.row('Четвер','П\'ятниця','Тиждень')
    return key

def groups_for_year(year):
    group_list = data.get_groups_for_year(year)
    groups = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard=True)
    for i in group_list:
        groups.row(i)
    return groups

def departments():
    deps = constants.departments
    key = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard=True)
    for i in deps:
        key.row(i)
    return key

def email_dep():
    dep_list = data.emails_deplist()
    deps = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard=True)
    for i in dep_list:
        deps.row(i)
    return deps

def email_name(dep):
    name_list = data.emails_namelist(dep)
    names = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard=True)
    for i in name_list:
        names.row(i)
    return names


def lib_years(chat_id):
    list = data.get_lib_years()
    list.sort()
    if len(list) != 0:
        key = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard=True)
        if len(storage.libGetChoosed(chat_id)) != 0:
            key.row('Отримати літературу')
        for i in list:
            key.row(i[0])
        return key
    else:
        return None

def lib_lessons(year, chat_id):
    list = data.get_lib_lessons(year)
    if len(list) != 0:
        key = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard=True)
        if len(storage.libGetChoosed(chat_id)) != 0:
            key.row('Отримати літературу')
        for i in list:
            key.row(i[0])
        return key
    else:
        return None

def lib_aus(year, lesson, chat_id):
    aus, names = data.get_lib_aus(year, lesson)
    if len(aus) != 0 or len(names) != 0:
        key = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard=True)
        if len(storage.libGetChoosed(chat_id)) != 0:
            key.row('Отримати літературу')
        for i in aus:
            key.row(i[0])
        for i in names:
            key.row(i[0])
        return key
    else:
        return None

def lib_files(year, lesson, aus, chat_id):
    names = data.get_lib_names(year, lesson, aus)
    if len(aus) != 0 or len(names) != 0:
        key = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard=True)
        if len(storage.libGetChoosed(chat_id)) != 0:
            key.row('Отримати літературу')
        for i in names:
            key.row(i[0])
        return key
    else:
        return None

def minka_key():
    # Список курсів
    key = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
    key.row('Ще питання')
    key.row('Хватє')
    return key

def minkasem_key():
    # Список курсів
    key = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
    key.row('1 семестр')
    key.row('2 семестр')
    key.row('Обидва')
    return key

def sport_sch_key():
    files = [file[:-4] for file in os.listdir("sport/")].sort()
    key = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
    for file in files:
        key.row(file)
    return key
