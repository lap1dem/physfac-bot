import constants as c
from modules import database

def translate_day(ukr_day):
    if ukr_day == c.week_days[0]:
        return 'monday.jpg'
    elif ukr_day == c.week_days[1]:
        return 'tuesday.jpg'
    elif ukr_day == c.week_days[2]:
        return 'wednesday.jpg'
    elif ukr_day == c.week_days[3]:
        return 'thursday.jpg'
    elif ukr_day == c.week_days[4]:
        return 'friday.jpg'
    elif ukr_day == c.week_days[5]:
        return ['monday.jpg','tuesday.jpg','wednesday.jpg','thursday.jpg','friday.jpg']

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
