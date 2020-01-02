# Defining bot
from hidden_data import * #imported token and DATABASE_URL
import telebot
bot = telebot.TeleBot(token)

# Project paths
shelve_name = 'local_data/shelve.db'

sch_path = 'local_data/schedule'
sport_sch_path = 'local_data/sport/'
clinic_sch_path = 'local_data/polyclinic/'
exams_sch_path = 'local_data/session_sch/'
