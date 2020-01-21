from implib import *
import modules.data_access as data
import modules.navigation as nav

work_dir = os.getcwd()

def stud_years():
    # Список курсів
    key = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
    key.row('1 курс','2 курс')
    key.row('3 курс','4 курс')
    key.row(' 1 курс м.','2 курс м.')
    key.row('Вчителі фізики (Туркменістан)')
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
    deps = c.departments
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
        if len(nav.libGetChoosed(chat_id)) != 0:
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
        if len(nav.libGetChoosed(chat_id)) != 0:
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
        if len(nav.libGetChoosed(chat_id)) != 0:
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
        if len(nav.libGetChoosed(chat_id)) != 0:
            key.row('Отримати літературу')
        for i in names:
            key.row(i[0])
        return key
    else:
        return None

def minka_key():
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
    files = [file[:-4] for file in os.listdir(sport_sch_path)]
    key = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
    for file in files:
        key.row(file)
    return key

def civ_ncivs_key():
    civs = ['5', '4', '3', '2', '1']
    key = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for i in civs:
        key.row(i)
    return key

def custom_key(buts):
    key = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    for b in buts:
        key.row(b)

    return key

def sch_plus_years():
    years = data.sch_get_years()
    # TODO: sort years
    key = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    for y in years:
        key.row(y)

    return key

def sch_plus_groups(chat_id):
    year = nav.sch_get_year(chat_id)
    groups = data.sch_get_groups(year)
    key = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    for g in groups:
        key.row(g)

    return key

def sch_plus_days(chat_id):
    year = nav.sch_get_year(chat_id)
    group = nav.sch_get_group(chat_id)
    days = data.sch_get_days(year, group)
    key = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    for d in days:
        key.row(d)

    return key