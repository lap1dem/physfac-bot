from implib import *

def translate_day(ukr_day):
    if ukr_day == c.week_days[0]:
        return 'monday.png'
    elif ukr_day == c.week_days[1]:
        return 'tuesday.png'
    elif ukr_day == c.week_days[2]:
        return 'wednesday.png'
    elif ukr_day == c.week_days[3]:
        return 'thursday.png'
    elif ukr_day == c.week_days[4]:
        return 'friday.png'
    elif ukr_day == c.week_days[5]:
        return ['monday.png','tuesday.png','wednesday.png','thursday.png','friday.png']

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
