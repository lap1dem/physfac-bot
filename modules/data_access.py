from implib import *
from constants import *

import modules.help_functions as help


# Wrapper for connecting to database
def data_conn(to_execute):
    def wrapper(*args):
        conn = psql.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        res = to_execute(conn, cur, *args)
        if (conn):
            cur.close()
            conn.close()
        return res

    return wrapper


# Creating tables
@data_conn
def ctemails(conn, cur):
    query = """CREATE TABLE IF NOT EXISTS emails
            (name TEXT NOT NULL,
            department TEXT NOT NULL,
            email TEXT NOT NULL)"""
    cur.execute(query)
    conn.commit()


ctemails()


@data_conn
def ctlibrary(conn, cur):
    query = """CREATE TABLE IF NOT EXISTS library
            (name TEXT NOT NULL,
            link TEXT NOT NULL,
            year TEXT NOT NULL,
            lesson TEXT NOT NULL,
            aus TEXT NOT NULL)"""
    cur.execute(query)
    conn.commit()


ctlibrary()


@data_conn
def ctusers(conn, cur):
    query = """CREATE TABLE IF NOT EXISTS users
            (id INT NOT NULL,
            username TEXT,
            name TEXT NOT NULL,
            year TEXT,
            stgroup TEXT,
            isadmin BOOLEAN,
            schtime TIME)"""
    cur.execute(query)
    conn.commit()


ctusers()



@data_conn
def ctnord(conn, cur):
    query = """CREATE TABLE IF NOT EXISTS nord
            (day INT,
            month INT,
            year INT,
            isnumerator BOOLEAN)"""
    cur.execute(query)
    conn.commit()


ctnord()


@data_conn
def ctpasswords(conn, cur):
    query = """CREATE TABLE IF NOT EXISTS passwords
            (func TEXT NOT NULL,
             password TEXT NOT NULL)"""
    cur.execute(query)


ctpasswords()


@data_conn
def get_list(conn, cur, table):
    cur.execute("SELECT * FROM {}".format(table))
    rows = cur.fetchall()
    return rows


# -----EMAILS--------------------
@data_conn
def get_email(conn, cur, name, dep):
    cur.execute("SELECT email FROM emails WHERE name = %s AND department = %s", (name, dep,))
    email = cur.fetchall()
    try:
        return email[0][0]
    except IndexError:
        return None


@data_conn
def get_all_emails(conn, cur):
    cur.execute("SELECT * FROM emails")
    all = cur.fetchall()

    with open("allemails.txt", "w+") as file:
        file.write("Ім'я,Пошта,Кафедра\n")
        for i in range(len(all)):
            file.write(
                all[i][0] + "," + all[i][2] + "," + all[i][1] + "\n"
            )

    return (None)


@data_conn
def add_email(conn, cur, name, dep, email):
    if not bool(get_email(name, dep)):
        cur.execute("INSERT INTO emails (name, department, email) VALUES (%s, %s, %s)", (name, dep, email,))
    else:
        pass
    conn.commit()


@data_conn
def emails_deplist(conn, cur):
    cur.execute("SELECT DISTINCT department FROM emails")
    deps = cur.fetchall()
    final_deps = []
    for i in deps:
        final_deps.append(i[0])
    return final_deps


@data_conn
def emails_namelist(conn, cur, dep):
    cur.execute("SELECT DISTINCT name FROM emails WHERE department = %s", (dep,))
    names = cur.fetchall()
    final_names = []
    for i in names:
        final_names.append(i[0])
    return final_names


@data_conn
def email_remove(conn, cur, name, dep):
    cur.execute("DELETE FROM emails WHERE name = %s AND department = %s", (name, dep,))
    conn.commit()


@data_conn
def search_by_name(conn, cur, query):
    cap_q = help.capitalize_n(query, 1)
    cur.execute('SELECT name, email FROM emails WHERE name LIKE %s', (cap_q,))
    row = cur.fetchall()
    return row


# ---LIBRARY--------------------
@data_conn
def get_lib_years(conn, cur):
    cur.execute("SELECT DISTINCT year FROM library")
    years = cur.fetchall()
    return years


@data_conn
def get_lib_lessons(conn, cur, year):
    year = year.split(",")[0]
    cur.execute("SELECT DISTINCT lesson FROM library WHERE year = %s", (year,))
    lessons = cur.fetchall()
    return lessons


@data_conn
def get_lib_aus(conn, cur, year, lesson):
    year = year.split(",")[0]
    cur.execute("SELECT DISTINCT aus FROM library WHERE year = %s AND lesson = %s AND NOT aus = %s",
                (year, lesson, '*',))
    aus = cur.fetchall()
    cur.execute("SELECT DISTINCT name FROM library WHERE year = %s AND lesson = %s AND aus = %s", (year, lesson, '*',))
    names = cur.fetchall()
    return (aus, names)


@data_conn
def get_lib_names(conn, cur, year, lesson, aus):
    cur.execute("SELECT DISTINCT name FROM library WHERE year = %s AND lesson = %s AND aus = %s", (year, lesson, aus,))
    names = cur.fetchall()
    return names


@data_conn
def add_book(conn, cur, name, link, year, lesson, aus):
    if not bool(get_book(name)):
        for y in year.split(","):
            cur.execute("INSERT INTO library (name, link, year, lesson, aus) VALUES (%s,%s,%s,%s,%s)",
                        (name, link, y, lesson, aus,))
    else:
        pass
    conn.commit()


@data_conn
def get_book(conn, cur, name):
    cur.execute("SELECT link FROM library WHERE name = %s", (name,))
    link = cur.fetchall()
    try:
        return link[0]
    except IndexError:
        return None


@data_conn
def del_book(conn, cur, name):
    link = get_book(name)
    cur.execute("DELETE FROM library WHERE link = %s", (link,))
    conn.commit()


@data_conn
def delete_library_table(conn, cur):
    cur.execute("DROP TABLE library")
    conn.commit()


# --------USERS---------------
@data_conn
def check_reg(conn, cur, id, username, name):
    cur.execute("SELECT username FROM users WHERE id = %s", (id,))
    ids = cur.fetchall()
    if len(ids) == 0:
        user_reg(id, username, name)
    else:
        pass


@data_conn
def user_reg(conn, cur, id, username, name):
    cur.execute("INSERT INTO users (id, username, name, year, stgroup, isadmin) VALUES (%s,%s,%s,NULL,NULL,FALSE)",
                (id, username, name,))
    conn.commit()


@data_conn
def registrated_users(conn, cur):
    cur.execute("SELECT name FROM users")
    names = cur.fetchall()
    return names


@data_conn
def get_chat_ids(conn, cur):
    cur.execute("SELECT id FROM users")
    ids = cur.fetchall()
    return ids


@data_conn
def make_admin(conn, cur, id):
    cur.execute("UPDATE users SET isadmin = TRUE WHERE id = %s", (id,))
    conn.commit()


@data_conn
def check_admin(conn, cur, id):
    cur.execute("SELECT isadmin FROM users WHERE id = %s", (id,))
    isadmin = cur.fetchall()[0]
    return (isadmin[0])


@data_conn
def get_password(conn, cur, func):
    cur.execute("SELECT password FROM passwords WHERE func = %s", (func,))
    passw = cur.fetchall()
    return (passw[0][0])

@data_conn
def get_schtime(conn, cur, id):
    cur.execute(f"SELECT schtime FROM users WHERE id = {id}")
    schtime = cur.fetchall()[0]
    if schtime[0] is None:
        return None
    else:
        # return time.fromisoformat(schtime[0])
        return schtime[0]

@data_conn
def set_schtime(conn, cur, id, schtime):
    if schtime is None:
        cur.execute(f"UPDATE users SET schtime = NULL WHERE id = {id}")
    else:
        schtime = schtime.isoformat()
        cur.execute(f"UPDATE users SET schtime = '{schtime}' WHERE id = {id}")
    conn.commit()

@data_conn
def get_user_year(conn, cur, id):
    cur.execute(f"SELECT year FROM users WHERE id = {id}")
    year = cur.fetchall()[0]
    return year

@data_conn
def set_user_year(conn, cur, id, year):
    cur.execute(f"UPDATE users SET year = '{year}' WHERE id = {id}")
    conn.commit()

@data_conn
def get_user_group(conn, cur, id):
    cur.execute(f"SELECT stgroup FROM users WHERE id = {id}")
    group = cur.fetchall()[0]
    return group

@data_conn
def set_user_group(conn, cur, id, group):
    cur.execute(f"UPDATE users SET stgroup = '{group}' WHERE id = {id}")
    conn.commit()

@data_conn
def get_all_schtime(conn, cur):
    cur.execute(f"SELECT (id, schtime) FROM users WHERE schtime IS NOT NULL")
    res = cur.fetchall()
    return(res)


# ----------NORD----------
@data_conn
def set_numerator(conn, cur):
    cur.execute("DELETE FROM nord")
    today = date.today()
    cur.execute("INSERT INTO nord (day, month, year, isnumerator) VALUES (%s, %s, %s, TRUE)",
                (today.day, today.month, today.year))
    conn.commit()


@data_conn
def set_denominator(conn, cur):
    cur.execute("DELETE FROM nord")
    today = date.today()
    cur.execute("INSERT INTO nord (day, month, year, isnumerator) VALUES (%s, %s, %s, FALSE)",
                (today.day, today.month, today.year))
    conn.commit()


@data_conn
def get_nord(conn, cur):
    # returns boolean "is_numerator"
    cur.execute("SELECT * FROM nord")
    row = cur.fetchall()[0]
    set_date = date(row[2], row[1], row[0])
    today = date.today()
    delta = today - set_date
    nweeks = int((delta.days + set_date.weekday()) / 7)
    if (nweeks + 2) % 2 == 0:
        return (row[3])
    return (not row[3])


# =========================================
# ==============SCHEDULE===================
# =========================================

@data_conn
def sch_get_years(conn, cur):
    cur.execute("SELECT DISTINCT year FROM schedule{}{}".format(cur_year, cur_semester))
    years = cur.fetchall()
    years = [y[0] for y in years]
    k = ["1 курс", "2 курс", "3 курс", "4 курс", "1 курс магістри", "2 курс магістри"]
    years = sorted(years, key=k.index)
    return (years)


@data_conn
def sch_get_groups(conn, cur, year):
    cur.execute("SELECT DISTINCT groupname FROM schedule{}{} WHERE year = %s".format(cur_year, cur_semester), (year,))
    groups = cur.fetchall()
    groups = [g[0] for g in groups]
    groups = sorted(groups)
    return (groups)


@data_conn
def sch_get_days(conn, cur, year, group):
    cur.execute(
        "SELECT DISTINCT day FROM schedule{}{} WHERE year = %s AND groupname = %s".format(cur_year, cur_semester),
        (year, group,))
    days = cur.fetchall()
    days = [d[0] for d in days]
    k = ["Понеділок", "Вівторок", "Середа", "Четвер", "П'ятниця", "Субота", "Неділя",]
    days = sorted(days, key=k.index)
    return (days)


@data_conn
def sch_get_lessons(conn, cur, year, group, day):
    cur.execute(
        "SELECT * FROM schedule{}{} WHERE year = %s AND groupname = %s AND day = %s".format(cur_year, cur_semester),
        (year, group, day,))
    lessons = cur.fetchall()

    df = pd.DataFrame(
        lessons, columns=[
            "year",
            "day",
            "groupname",
            "leshead",
            "lesnum",
            "timestart",
            "timeend",
            "lesname",
            "aud",
            "teach",
            "sg",
            "half",
        ]
    )

    df.sort_values(by=['lesnum', 'half', 'sg'], na_position='first', inplace=True)

    return (df)
