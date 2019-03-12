
import shelve as sh
import database as db
from config import *


# ------------------SCHEDULE----------------------------------

def update_schedule_path(chat_id,repository):
    with sh.open(shelve_name) as storage:
        try:
            cur_path = storage['sch'+str(chat_id)]
            storage['sch'+str(chat_id)] = cur_path + '/' + repository
        except KeyError:
            storage['sch'+str(chat_id)] = repository

def del_schedule_path(chat_id):
    with sh.open(shelve_name) as storage:
        try:
            del storage['sch'+str(chat_id)]
        except KeyError:
            pass

def get_schedule_path(chat_id):
    with sh.open(shelve_name) as storage:
        try:
            return storage['sch'+str(chat_id)]
        except KeyError:
            return None

# ---------------EMAILS-----------------------------

def upd_ename(chat_id, name):
    with sh.open(shelve_name) as storage:
            storage['ename'+str(chat_id)] = name

def upd_edep(chat_id, dep):
    with sh.open(shelve_name) as storage:
            storage['edep'+str(chat_id)] = dep

def del_edata(chat_id):
    with sh.open(shelve_name) as storage:
        try:
            del storage['ename'+str(chat_id)]
            del storage['edep'+str(chat_id)]
        except KeyError:
            pass

def get_edep(chat_id):
    with sh.open(shelve_name) as storage:
        try:
            dep = storage['edep'+str(chat_id)]
            return dep
        except KeyError:
            return None

def get_edata(chat_id):
    with sh.open(shelve_name) as storage:
        try:
            name = storage['ename'+str(chat_id)]
            dep = storage['edep'+str(chat_id)]
            return (name, dep)
        except KeyError:
            return None

# -------------OTHER--------------------------------
def check_running(chat_id):
    with sh.open(shelve_name) as storage:
        try:
            key_check = storage["run_"+str(chat_id)]
            return True
        except KeyError:
            return False
