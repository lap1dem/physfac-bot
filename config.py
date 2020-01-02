# Defining bot
import telebot
token = '934435638:AAEDGw89ytOeGOdUFLFaVQL86aotsNKGtW4'
bot = telebot.TeleBot(token)

# Project paths
shelve_name = 'local_data/shelve.db'

sch_path = 'local_data/schedule'
sport_sch_path = 'local_data/sport/'
clinic_sch_path = 'local_data/polyclinic/'
exams_sch_path = 'local_data/session_sch/'
