import sqlite3 as sq
import os
import help_functions as help
from config import *

def create_lists():
    conn = sq.connect(database_name)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS 'users' (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, chat_id INTEGER NOT NULL)")
    cur.execute("CREATE TABLE IF NOT EXISTS 'years_and_groups' (year TEXT NOT NULL, groups TEXT NOT NULL)")
    cur.execute("CREATE TABLE IF NOT EXISTS 'emails' (name TEXT NOT NULL, department TEXT NOT NULL, email TEXT NOT NULL)")
    cur.execute("CREATE TABLE IF NOT EXISTS 'library' (name TEXT NOT NULL, link TEXT NOT NULL, year TEXT NOT NULL, lesson TEXT NOT NULL, aus TEXT)")
    conn.commit()
    conn.close()

create_lists()

class SQL:
    def __init__(self,database_name):
        self.conn = sq.connect(database_name)
        self.cur = self.conn.cursor()

    def get_list(self,table):
        # with self.conn:
        self.cur.execute("SELECT * FROM {}".format(table))
        rows = self.cur.fetchall()
        return rows

    def select_all(self,table):
        # with self.conn:
        self.cur.execute('SELECT * FROM {}'.format(table))
        row = self.cur.fetchall()
        return row


    def select_single(self,table,rownum):
        # with self.conn:
        self.cur.execute('SELECT * FROM {} WHERE id = ?'.format(table),(rownum,))
        row = self.cur.fetchall()
        return row

    def count_rows(self,table):
        # with self.conn:
        self.cur.execute('SELECT * FROM {}'.format(table))
        result = self.cur.fetchall()
        return len(result)

# ------SENT FILES-------------------------------------------------------------------------------

    def sent_files_check(self,path):
        self.cur.execute('SELECT * FROM "sent_files" WHERE path_to_file = ?',(path,))#!!!!!!!!!!!
        sent_files = self.cur.fetchall()
        return bool(len(sent_files))

    def sent_files_get_id(self,path):
        self.cur.execute('SELECT * FROM "sent_files" WHERE path_to_file = ?',(path,))
        sent_files = self.cur.fetchall()
        return sent_files[0][1]

    def sent_files_add(self,path,file_id):
        self.cur.execute("INSERT INTO 'sent_files' (file_id,path_to_file) VALUES (?,?)",(file_id,path,))
        self.conn.commit()

# --------REGISTRATION------------------------------------------------------------------------------

    def add_user(self,chat_id):
        if not self.check_user(chat_id):
            self.cur.execute("INSERT INTO 'users' (chat_id) VALUES (?)",(chat_id,))
            self.conn.commit()

    def check_user(self,chat_id):
        self.cur.execute("SELECT * FROM 'users' WHERE chat_id = ?",(chat_id,))
        user = self.cur.fetchall()
        return len(user)

# --------EMAILS-------------------------------------------------------------------------------
    def get_email(self, name, dep):
        self.cur.execute("SELECT email FROM 'emails' WHERE name = ? AND department = ?",(name,dep,))
        email = self.cur.fetchall()
        try:
            return email[0][0]
        except IndexError:
            return None

    def add_email(self, name, dep, email):
        if not bool(self.get_email(name, dep)):
            self.cur.execute("INSERT INTO 'emails' (name, department, email) VALUES (?,?,?)",(name, dep, email,))
        else:
            pass
        self.conn.commit()

    def emails_deplist(self):
        self.cur.execute("SELECT DISTINCT department FROM 'emails'")
        deps = self.cur.fetchall()
        final_deps = []
        for i in deps:
            final_deps.append(i[0])
        return final_deps

    def emails_namelist(self, dep):
        self.cur.execute("SELECT DISTINCT name FROM 'emails' WHERE department = ?",(dep,))
        names = self.cur.fetchall()
        final_names = []
        for i in names:
            final_names.append(i[0])
        return final_names

    def email_remove(self, name, dep):
        self.cur.execute("DELETE FROM 'emails' WHERE name = ? AND department = ?",(name,dep,))
        self.conn.commit()

    def search_by_name(self, query):
        cap_q = help.capitalize_n(query, 2)
        self.cur.execute('SELECT name, email FROM emails WHERE name LIKE {}'.format(cap_q,))
        row = self.cur.fetchall()
        return row

# ---LIBRARY--------------------
    def get_lib_years(self):
        self.cur.execute("SELECT DISTINCT year FROM library")
        years = self.cur.fetchall()
        return years

    def get_lib_lessons(self, year):
        self.cur.execute("SELECT DISTINCT lesson FROM library WHERE year = ?", (year,))
        lessons = self.cur.fetchall()
        return lessons

    def get_lib_aus(self, year, lesson):
        self.cur.execute("SELECT DISTINCT aus FROM library WHERE year = ? AND lesson = ?", (year, lesson,))
        aus = self.cur.fetchall()
        return aus

    def add_book(self, name, link, year, lesson, aus):
        if not bool(self.get_book(name)):
            self.cur.execute("INSERT INTO 'library' (name, link, year, lesson, aus) VALUES (?,?,?,?,?)",(name, link, year, lesson, aus,))
        else:
            pass
        self.conn.commit()

    def get_book(self, name):
        self.cur.execute("SELECT link FROM library WHERE name = ?", (name,))
        link = self.cur.fetchall()
        try:
            return link[0]
        except IndexError:
            return None

    def close(self):
        self.conn.close()
