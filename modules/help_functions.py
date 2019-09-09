import constants as c

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
