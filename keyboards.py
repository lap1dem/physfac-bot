from telebot.types import (
    ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
)
from config import *
import constants
import database

def stud_years():
    # Список курсів
    return ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True).row('1 курс','2 курс').row('3 курс','4 курс').row(' 1 курс м.','2 курс м.')

def week_days():
    # Список робочих днів
    return ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True).row('Понеділок','Вівторок','Середа',).row('Четвер','П\'ятниця','Тиждень')

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
