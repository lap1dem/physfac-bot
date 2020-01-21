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

def check_line_length(line):
    if len(line) > 25:
        parts = line.split(' ')
        res = ''
        line = ''
        for i in range(len(parts)):
            line += ' '+parts[i]
            if i == 0:
                line = line[1:]

            if len(line) > 16 or i == len(parts)-1:
                res += line
                line = ''
                if not i == len(parts)-1:
                    res += '\n \t\t\t\t\t\t\t\t'

        return res
    else:
        return line

def create_sch_message(df):
    join = '├ '
    end = '└ '
    dash = '┊ '
    msg = '*' + df['day'][0] + '*\n'

    #         "year",
    #         "day",
    #         "groupname",
    #         "leshead",
    #         "lesnum",
    #         "timestart",
    #         "timeend",
    #         "lesname",
    #         "aud",
    #         "teach",
    #         "sg",
    #         "half",

    for i in range(1,5):
        lesnum = df.loc[df['lesnum'] == i]
        mod = ''

        if len(df.loc[df['lesnum'] == i])==0:
            continue

        if i == 4 or len(df.loc[df['lesnum'] == i+1])==0:
            lesmsg = end + '*' + lesnum['leshead'].values[0] + '*\n'
        else:
            lesmsg = join + '*' + lesnum['leshead'].values[0] + '*\n'

        if not end in lesmsg:
            mod += dash + '\t'
        else:
            mod += '\t\t\t'

        time = "_{:02d}:{:02d}-{:02d}:{:02d}_".format(
            lesnum['timestart'].values[0].hour,
            lesnum['timestart'].values[0].minute,
            lesnum['timeend'].values[0].hour,
            lesnum['timeend'].values[0].minute,
        )

        lesmsg += mod + join + time + '\n'

        h1 = lesnum.loc[(df['half'] == 1) & (df.isna()['sg'] == True)]
        h2 = lesnum.loc[(df['half'] == 2) & (df.isna()['sg'] == True)]

        s1 = lesnum.loc[(df.isna()['half'] == True) & (df['sg'] == 1)]
        s2 = lesnum.loc[(df.isna()['half'] == True) & (df['sg'] == 2)]

        h1s1 = lesnum.loc[(df['half'] == 1) & (df['sg'] == 1)]
        h1s2 = lesnum.loc[(df['half'] == 1) & (df['sg'] == 2)]
        h2s1 = lesnum.loc[(df['half'] == 2) & (df['sg'] == 1)]
        h2s2 = lesnum.loc[(df['half'] == 2) & (df['sg'] == 2)]

        if not False in [x.empty for x in [h1,h2,s1,s2,h1s1,h1s2,h2s1,h2s2]]:
            if lesnum['aud'].values[0] != None:
                lesmsg += check_line_length(mod + join + lesnum['aud'].values[0] + '\n')
            if lesnum['teach'].values[0] == None:
                lesmsg += check_line_length(mod + end + lesnum['lesname'].values[0] + '\n')
            else:
                lesmsg += check_line_length(mod + join + lesnum['lesname'].values[0] + '\n')
                lesmsg += mod + end + lesnum['teach'].values[0] + '\n'

        else:
            # ЧИСЕЛЬНИК
            if not h1.empty:
                if h2.empty and h2s1.empty and h2s2.empty:
                    lesmsg += mod + end + '*Чисельник*' + '\n'
                    mod += '\t\t'
                else:
                    lesmsg += mod + join + '*Чисельник*' + '\n'
                    mod += dash + '\t'

                if h1['aud'].values[0] != None:
                    lesmsg += check_line_length(mod + join + h1['aud'].values[0] + '\n')
                if h1['teach'].values[0] == None:
                    lesmsg += check_line_length(mod + end + h1['lesname'].values[0] + '\n')
                else:
                    lesmsg += check_line_length(mod + join + h1['lesname'].values[0] + '\n')
                    lesmsg += mod + end + h1['teach'].values[0] + '\n'

                mod = mod[:-3]

            if not s1.empty:
                if s2.empty and h1s2.empty and h2s2.empty:
                    lesmsg += mod + end + '*1-а підгрупа*' + '\n'
                    mod += '\t\t'
                else:
                    lesmsg += mod + join + '*1-а підгрупа*' + '\n'
                    mod += dash + '\t'

                if s1['aud'].values[0] != None:
                    lesmsg += check_line_length(mod + join + s1['aud'].values[0] + '\n')
                if s1['teach'].values[0] == None:
                    lesmsg += check_line_length(mod + end + s1['lesname'].values[0] + '\n')
                else:
                    lesmsg += check_line_length(mod + join + s1['lesname'].values[0] + '\n')
                    lesmsg += mod + end + s1['teach'].values[0] + '\n'


                mod = mod[:-3]

            if not h1s1.empty or not h1s2.empty:
                if h2.empty and h2s1.empty and h2s2.empty:
                    lesmsg += mod + end + '*Чисельник*' + '\n'
                    mod += '\t\t'
                else:
                    lesmsg += mod + join + '*Чисельник*' + '\n'
                    mod += dash + '\t'


                if not h1s1.empty:
                    if h1s2.empty:
                        lesmsg += mod + end + '*1-а підгрупа*' + '\n'
                        mod += '\t\t'
                    else:
                        lesmsg += mod + join + '*1-а підгрупа*' + '\n'
                        mod += dash + '\t'

                    if h1s1['aud'].values[0] != None:
                        lesmsg += check_line_length(mod + join + h1s1['aud'].values[0] + '\n')
                    if h1s1['teach'].values[0] == None:
                        lesmsg += check_line_length(mod + end + h1s1['lesname'].values[0] + '\n')
                    else:
                        lesmsg += check_line_length(mod + join + h1s1['lesname'].values[0] + '\n')
                        lesmsg += mod + end + h1s1['teach'].values[0] + '\n'

                        mod = mod[:-2]

                if not h1s2.empty:
                    lesmsg += mod + end + '*2-а підгрупа*' + '\n'
                    mod += '\t\t'

                    if h1s2['aud'].values[0] != None:
                        lesmsg += check_line_length(mod + join + h1s2['aud'].values[0] + '\n')
                    if h1s2['teach'].values[0] == None:
                        lesmsg += check_line_length(mod + end + h1s2['lesname'].values[0] + '\n')
                    else:
                        lesmsg += check_line_length(mod + join + h1s2['lesname'].values[0] + '\n')
                        lesmsg += mod + end + h1s2['teach'].values[0] + '\n'

                    mod = mod[:-2]

                mod = mod[:-2]

            if not s2.empty:
                lesmsg += mod + end + '*2-а підгрупа*' + '\n'
                mod += '\t\t'

                if s2['aud'].values[0] != None:
                    lesmsg += check_line_length(mod + join + s2['aud'].values[0] + '\n')
                if s2['teach'].values[0] == None:
                    lesmsg += check_line_length(mod + end + s2['lesname'].values[0] + '\n')
                else:
                    lesmsg += check_line_length(mod + join + s2['lesname'].values[0] + '\n')
                    lesmsg += mod + end + s2['teach'].values[0] + '\n'

                mod = mod[:-2]

            # ЗНАМЕННИК
            if not h2.empty:
                lesmsg += mod + end + '*Знаменник*' + '\n'
                mod += '\t\t'

                if h2['aud'].values[0] != None:
                    lesmsg += (mod + join + h2['aud'].values[0] + '\n')
                if h2['teach'].values[0] == None:
                    lesmsg += check_line_length(mod + end + h2['lesname'].values[0] + '\n')
                else:
                    lesmsg += check_line_length(mod + join + h2['lesname'].values[0] + '\n')
                    lesmsg += mod + end + h2['teach'].values[0] + '\n'

                mod = mod[:-2]

            if not h2s1.empty or not h2s2.empty:
                lesmsg += mod + join + '*Знаменник*' + '\n'
                mod += '\t\t'

                if not h2s1.empty:
                    if h2s2.empty:
                        lesmsg += mod + end + '*1-а підгрупа*' + '\n'
                        mod += '\t\t'
                    else:
                        lesmsg += mod + join + '*1-а підгрупа*' + '\n'
                        mod += dash + '\t'

                    if h2s1['aud'].values[0] != None:
                        lesmsg += check_line_length(mod + join + h2s1['aud'].values[0] + '\n')
                    if h2s1['teach'].values[0] == None:
                        lesmsg += check_line_length(mod + end + h2s1['lesname'].values[0] + '\n')
                    else:
                        lesmsg += check_line_length(mod + join + h2s1['lesname'].values[0] + '\n')
                        lesmsg += mod + end + h2s1['teach'].values[0] + '\n'

                    mod = mod[:-3]

                if not h2s2.empty:
                    lesmsg += mod + end + '*2-а підгрупа*' + '\n'
                    mod += '\t\t'

                    if h2s2['aud'].values[0] != None:
                        lesmsg += check_line_length(mod + join + h2s2['aud'].values[0] + '\n')
                    if h2s2['teach'].values[0] == None:
                        lesmsg += check_line_length(mod + end + h2s2['lesname'].values[0] + '\n')
                    else:
                        lesmsg += check_line_length(mod + join + h2s2['lesname'].values[0] + '\n')
                        lesmsg += mod + end + h2s2['teach'].values[0] + '\n'

                    mod = mod[:-2]

                mod = mod[:-2]



        if not (i == 4 or len(df.loc[df['lesnum'] == i+1])==0):
            lesmsg += dash + '\n'
        msg += lesmsg
    return(msg)



