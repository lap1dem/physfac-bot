# %%
import psycopg2 as psql
import os
import modules.help_functions as help

DATABASE_URL = os.environ['DATABASE_URL']

# %%
def data_conn(to_execute):
    def wrapper(*args):
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            cur = conn.cursor()

            res = to_execute(conn, cur, *args)

        except (Exception, psql.DatabaseError) as error :
            print ("Error while executing " + to_execute.__name__ +"()", error)

        finally:
                if(conn):
                    cur.close()
                    conn.close()
                return res

    return wrapper


@data_conn
def ctemails(conn, cur):
    query = """CREATE TABLE IF NOT EXISTS emails
            (name TEXT NOT NULL,
            department TEXT NOT NULL,
            email TEXT NOT NULL)"""
    cur.execute(query)
    conn.commit()

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

@data_conn
def get_list(conn, cur, table):
    cur.execute("SELECT * FROM {}".format(table))
    rows = cur.fetchall()
    return rows
# -----EMAILS--------------------
@data_conn
def get_email(conn, cur, name, dep):
    cur.execute("SELECT email FROM emails WHERE name = %s AND department = %s",(name,dep,))
    email = cur.fetchall()
    try:
        return email[0][0]
    except IndexError:
        return None

@data_conn
def add_email(conn, cur, name, dep, email):
    if not bool(get_email(name, dep)):
        cur.execute("INSERT INTO emails (name, department, email) VALUES (%s, %s, %s)",(name, dep, email,))
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
    cur.execute("SELECT DISTINCT name FROM emails WHERE department = %s",(dep,))
    names = cur.fetchall()
    final_names = []
    for i in names:
        final_names.append(i[0])
    return final_names

@data_conn
def email_remove(conn, cur, name, dep):
    cur.execute("DELETE FROM emails WHERE name = %s AND department = %s",(name,dep,))
    conn.commit()

@data_conn
def search_by_name(conn, cur, query):
    cap_q = help.capitalize_n(query, 1)
    cur.execute('SELECT name, email FROM emails WHERE name LIKE %s',(cap_q,))
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
    cur.execute("SELECT DISTINCT lesson FROM library WHERE year = %s", (year,))
    lessons = cur.fetchall()
    return lessons

@data_conn
def get_lib_aus(conn, cur, year, lesson):
    cur.execute("SELECT DISTINCT aus FROM library WHERE year = %s AND lesson = %s AND NOT aus = %s", (year, lesson, '*',))
    aus = cur.fetchall()
    cur.execute("SELECT DISTINCT name FROM library WHERE year = %s AND lesson = %s AND aus = %s", (year, lesson,'*',))
    names = cur.fetchall()
    return (aus, names)

@data_conn
def get_lib_names(conn, cur, year, lesson, aus):
    cur.execute("SELECT DISTINCT name FROM library WHERE year = %s AND lesson = %s AND aus = %s", (year, lesson,aus,))
    names = cur.fetchall()
    return names

@data_conn
def add_book(conn, cur, name, link, year, lesson, aus):
    if not bool(get_book(name)):
        cur.execute("INSERT INTO library (name, link, year, lesson, aus) VALUES (%s,%s,%s,%s,%s)",(name, link, year, lesson, aus,))
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


# %%
get_lib_aus('3 курс', 'Ядерна фізика')
