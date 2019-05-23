import shelve as sh
from modules import database as db
from config import *
import os
import json


def delete_all(chat_id):
    with sh.open(shelve_name) as storage:
        keys = list(storage.keys())
        todel = [key for key in keys if str(chat_id) in key]
        for key in todel:
            del storage[key]

# ------------------SCHEDULE----------------------------------

def update_schedule_path(chat_id,repository):
    with sh.open(shelve_name) as storage:
        try:
            cur_path = storage['sch'+str(chat_id)]
            storage['sch'+str(chat_id)] = cur_path + '/' + repository
        except KeyError:
            storage['sch'+str(chat_id)] = repository

def replace_schedule_path(chat_id, path):
    with sh.open(shelve_name) as storage:
        storage['sch'+str(chat_id)] = path

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

def schedule_step_back(chat_id):
    cur_path = get_schedule_path(chat_id)
    new_path = os.path.split(cur_path)[0]
    replace_schedule_path(chat_id, new_path)



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

# -----------OLD-LIBRARY-----------------------------
def update_lib_path(chat_id,repository):
    with sh.open(shelve_name) as storage:
        try:
            cur_path = storage['lib'+str(chat_id)]
            storage['lib'+str(chat_id)] = cur_path + '/' + repository
        except KeyError:
            storage['lib'+str(chat_id)] = repository

def del_lib_path(chat_id):
    with sh.open(shelve_name) as storage:
        try:
            del storage['lib'+str(chat_id)]
        except KeyError:
            pass

def get_lib_path(chat_id):
    with sh.open(shelve_name) as storage:
        try:
            return storage['lib'+str(chat_id)]
        except KeyError:
            return None

def replace_lib_path(chat_id, path):
    with sh.open(shelve_name) as storage:
        storage['lib'+str(chat_id)] = path

def lib_step_back(chat_id):
    cur_path = get_lib_path(chat_id)
    new_path = os.path.split(cur_path)[0]
    replace_lib_path(chat_id, new_path)

def lib_at_start(chat_id):
    if os.path.split(get_lib_path(chat_id))[0] == '':
        return True
    return False

# -----------NEW-LIBRARY-----------------------------
def libUpdName(chat_id, name):
    with sh.open(shelve_name) as storage:
        try:
            names = json.loads(storage['lib_n'+str(chat_id)])
            names.append(name)
            storage['lib_n'+str(chat_id)] = json.dumps(names)
        except KeyError:
            storage['lib_n'+str(chat_id)] = json.dumps([name])

def libUpdLink(chat_id, link):
    with sh.open(shelve_name) as storage:
        try:
            links = json.loads(storage['lib_link'+str(chat_id)])
            links.append(link)
            storage['lib_link'+str(chat_id)] = json.dumps(links)
        except KeyError:
            storage['lib_link'+str(chat_id)] = json.dumps([link])

def libSetYear(chat_id, year):
    with sh.open(shelve_name) as storage:
        storage['lib_y'+str(chat_id)] = year

def libSetLesson(chat_id, lesson):
    with sh.open(shelve_name) as storage:
        storage['lib_l'+str(chat_id)] = lesson

def libSetAus(chat_id, aus):
    with sh.open(shelve_name) as storage:
        storage['lib_a'+str(chat_id)] = aus

def libGetYear(chat_id):
    with sh.open(shelve_name) as storage:
        try:
            return storage['lib_y'+str(chat_id)]
        except KeyError:
            return None

def libGetLesson(chat_id):
    with sh.open(shelve_name) as storage:
        try:
            return storage['lib_l'+str(chat_id)]
        except KeyError:
            return None

def libGetAll(chat_id):
    with sh.open(shelve_name) as storage:
        names = json.loads(storage['lib_n'+str(chat_id)])
        links = json.loads(storage['lib_link'+str(chat_id)])
        year = storage['lib_y'+str(chat_id)]
        lesson = storage['lib_l'+str(chat_id)]
        aus = storage['lib_a'+str(chat_id)]
        return [names, links, year, lesson, aus]


# -------------OTHER--------------------------------
def check_running(chat_id):
    with sh.open(shelve_name) as storage:
        try:
            key_check = storage["run_"+str(chat_id)]
            return True
        except KeyError:
            return False

# def update_prev(chat_id, text):
#     with sh.open(shelve_name) as storage:
#         storage['prev'+str(chat_id)] = text
#
# def del_prev(chat_id):
#     with sh.open(shelve_name) as storage:
#         try:
#             del storage['prev'+str(chat_id)]
#         except KeyError:
#             pass
#
# def get_prev(chat_id):
#     with sh.open(shelve_name) as storage:
#         try:
#             return storage['prev'+str(chat_id)]
#         except KeyError:
#             return None
