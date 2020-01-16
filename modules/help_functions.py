from implib import *

def translate_day(ukr_day):
    if ukr_day == c.week_days[0]:
        return 'Monday.png'
    elif ukr_day == c.week_days[1]:
        return 'Tuesday.png'
    elif ukr_day == c.week_days[2]:
        return 'Wednesday.png'
    elif ukr_day == c.week_days[3]:
        return 'Thursday.png'
    elif ukr_day == c.week_days[4]:
        return 'Friday.png'
    elif ukr_day == c.week_days[5]:
        return ['Monday.png','Tuesday.png','Wednesday.png','Thursday.png','Friday.png']

def get_sch_folder(msg):
    if msg == '1 курс':
        return 'B1'
    elif msg == '2 курс':
        return 'B2'
    elif msg == '3 курс':
        return 'B3'
    elif msg == '4 курс':
        return 'B4'
    elif msg == '1 курс м.':
        return 'M1'
    elif msg == '2 курс м.':
        return 'M2'
    elif msg == 'Вчителі фізики (Туркменістан)':
        return 'T'
    else:
        return None

def capitalize_n(s,n):
    return s[:n]+ s[n].capitalize() + s[n+1:]

def get_sport_files():
    return [file[:-4] for file in os.listdir(sport_sch_path)]

def get_fullname(message):
    fullname = message.from_user.first_name
    try:
        fullname += ' '
        fullname += message.from_user.last_name
    except TypeError:
        pass
    return(fullname)

def log_to_dialog(message, function):
    if c.log_to_dialog:
        if message.chat.id != 394701484:
            fullname = help.get_fullname(message)
            bot.send_message(394701484, function + "\n" + fullname)
