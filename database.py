import sqlite3 as sq
import os
import help_functions as help
from config import *

def create_lists():
    conn = sq.connect(database_name)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS 'users' (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, chat_id INTEGER NOT NULL, year TEXT NOT NULL, groups TEXT NOT NULL, is_admin BOOL)")
    cur.execute("CREATE TABLE IF NOT EXISTS 'sent_files' (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, file_id TEXT NOT NULL, path_to_file TEXT NOT NULL)")
    cur.execute("CREATE TABLE IF NOT EXISTS 'years_and_groups' (year TEXT NOT NULL, groups TEXT NOT NULL)")
    cur.execute("CREATE TABLE IF NOT EXISTS 'emails' (name TEXT NOT NULL, department TEXT NOT NULL, email TEXT NOT NULL)")
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
        result = self.cur.execute('SELECT * FROM {}'.format(table))
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
        self.cur.execute("INSERT INTO 'sent_files' (file_id,path_to_file) VALUES (?,?)",(file_id,path))
        self.conn.commit()

# --------REGISTRATION------------------------------------------------------------------------------

    def reg_check(self,chat_id):
        self.cur.execute("SELECT * FROM 'users' WHERE chat_id = ?",(chat_id,))
        reg_users = self.cur.fetchall()
        return bool(ltn(reg_users))

    def add_user(self,chat_id,year,group,is_admin = False):
        self.cur.execute("INSERT INTO 'users' (chat_id,year,groups,is_admin) VALUES (?,?,?,?)",(chat_id,year,group,is_admin))
        self.conn.commit()

    def get_groups_for_year(self,year):
        self.cur.execute("SELECT * FROM 'years_and_groups' WHERE year = ?",(year,))
        groups = self.cur.fetchall()
        group_list = []
        for group in groups:
            group_list.append(group[1])
        return group_list

# --------EMAILS-------------------------------------------------------------------------------
    def get_email(self, name, dep):
        self.cur.execute("SELECT email FROM 'emails' WHERE name = ? AND department = ?",(name,dep))
        email = self.cur.fetchall()
        try:
            return email[0][0]
        except IndexError:
            return None

    def add_email(self, name, dep, email):
        if not bool(self.get_email(name, dep)):
            self.cur.execute("INSERT INTO 'emails' (name, department, email) VALUES (?,?,?)",(name, dep, email))
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
        self.cur.execute("DELETE FROM 'emails' WHERE name = ? AND department = ?",(name,dep))
        self.conn.commit()

    def search_by_name(self, query):
        cap_q = help.capitalize_n(query, 2)
        self.cur.execute('SELECT name, email FROM emails WHERE name LIKE {}'.format(cap_q,))
        row = self.cur.fetchall()
        return row


    def close(self):
        self.conn.close()
