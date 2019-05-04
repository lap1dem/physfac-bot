from telebot.types import (
    ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
)
from config import *
import constants
import database
import os
# import storage

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
    data = database.SQL(database_name)
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
    data = database.SQL(database_name)
    dep_list = data.emails_deplist()
    deps = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard=True)
    for i in dep_list:
        deps.row(i)
    return deps

def email_name(dep):
    data = database.SQL(database_name)
    name_list = data.emails_namelist(dep)
    names = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard=True)
    for i in name_list:
        names.row(i)
    return names

def library_list(path):
    list = os.listdir(work_dir + '/' + path)
    list.sort()
    liblist = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard=True)
    for i in list:
        liblist.row(i)
    return liblist
