import modules.data_access as data
import modules.help_functions as help

from implib import *

def send_day_sch():
    all_schtimes = help.tuple_from_string(data.get_all_schtime())
    now = datetime.now()
    send_to_users = []

    for user_set in all_schtimes:
        schtime = time.fromisoformat(user_set[1])

        if check_time_diff(now, schtime, 60):
            send_to_users.append(user_set)

    for user_set in send_to_users:
        day_ind = now.weekday()
        if now.hour >= 14:
            day_ind += 1
        day = c.week[day_ind]

        year = data.get_user_year(int(user_set[0]))
        group = data.get_user_group(int(user_set[0]))
        days = data.sch_get_days(year, group)
        day_found = False
        for d in days:
            if day in d:
                day = d
                day_found = True
        if day_found:
            lessons = data.sch_get_lessons(year, group, day)
            if not lessons.empty:
                msg = help.create_sch_message(lessons)
                is_num = data.get_nord()
                if is_num:
                    msg += "\nЦього тижня - _чисельник_."
                else:
                    msg += "\nЦього тижня - _знаменник_."
                bot.send_message(
                    int(user_set[0]),
                    msg,
                    parse_mode="Markdown",
                )
        else:
            pass