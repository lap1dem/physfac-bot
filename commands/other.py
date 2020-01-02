from implib import *

import modules.keyboards as key
import modules.navigation as nav
import modules.minka as minka
import modules.help_functions as help
import modules.data_access as data

# USER COMMANDS

@bot.message_handler(commands=['other'])
def other_comands(message):
    msg = "*Інші команди*:\n" + c.other_comands
    bot.send_message(
        message.chat.id,
        msg,
        parse_mode="Markdown"
    )

@bot.message_handler(commands=['qmminka'])
def qmminka_start(message):
    fullname = help.get_fullname(message)
    print('"qmminka" command has been used by ' + fullname)
    help.log_to_dialog(message, "qmminka")
    reply = key.minkasem_key()
    bot.send_message(
        message.chat.id, 'Мінка з КМ. Оберіть семестр.', reply_markup=reply)
    bot.register_next_step_handler(message, qmminka)


def qmminka(message):
    if message.text != 'Хватє' and message.text != 'Ще питання':
        nav.qmm_setsem(message.chat.id, message.text)
    if message.text == 'Хватє':
        key_rem = telebot.types.ReplyKeyboardRemove()
        bot.send_message(
            message.chat.id, 'Окей, удачі на мінці!', reply_markup=key_rem)
        bot.send_sticker(message.chat.id, 'CAADAgADaQADrKqGF8Qij6L82sPwAg')
    else:
        sem = nav.qmm_getsem(message.chat.id)
        reply = key.minka_key()
        que = minka.get_qm_question(sem)
        bot.send_message(message.chat.id, que, reply_markup=reply)
        bot.register_next_step_handler(message, qmminka)

@bot.message_handler(commands=['ttclinic'])
def ttpolyclinic(message):
    fullname = help.get_fullname(message)
    print('"ttclinic" command has been used by ' + fullname)
    help.log_to_dialog(message, "ttclinic")
    bot.send_message(message.chat.id, "Розклад роботи поліклініки:")
    files = os.listdir(clinic_sch_path)
    opened_files = []
    for file in files:
        opened_files.append(
            open(clinic_sch_path + file, 'rb')
        )
    input_media = [InputMediaPhoto(file) for file in opened_files]
    msg = bot.send_media_group(message.chat.id, input_media)
    for file in opened_files:
        file.close()
    msg_text = "Останнє оновлення розкладу: " + c.last_polyclinic_photos
    bot.send_message(message.chat.id, msg_text)


@bot.message_handler(commands=['ttsport'])
def ttsport(message):
    fullname = help.get_fullname(message)
    print('"ttsport" command has been used by ' + fullname)
    help.log_to_dialog(message, "ttsport")
    markup = key.sport_sch_key()
    bot.send_message(message.chat.id,
                     "Розклад роботи секцій спорткомплексу. Будь ласка, оберіть секцію.",
                     reply_markup=markup)
    bot.register_next_step_handler(message, send_sport_shchedule)


def send_sport_shchedule(message):
    if message.text in help.get_sport_files():
        key_rem = telebot.types.ReplyKeyboardRemove()
        schedule = open(sport_sch_path + message.text + '.jpg', 'rb')
        bot.send_photo(
            message.chat.id,
            schedule,
            reply_markup=key_rem
        )
        bot.send_message(
            message.chat.id, "Останнє оновлення розкладу: " + c.last_sport_photos)
    else:
        bot.send_message(
            message.chat.id, "Будь ласка, оберіть варіант зі списку.")
        bot.register_next_step_handler(message, send_sport_shchedule)


@bot.message_handler(commands=['nord'])
def nord(message):
    fullname = help.get_fullname(message)
    print('"nord" command has been used by ' + fullname)
    help.log_to_dialog(message, "nord")
    is_num = data.get_nord()
    if is_num:
        bot.send_message(message.chat.id, "Цього тижня - чисельник.")
    else:
        bot.send_message(message.chat.id, "Цього тижня - знаменник.")

@bot.message_handler(commands=['plasminka'])
def plasminka_start(message):
    fullname = help.get_fullname(message)
    print('"plasminka" command has been used by ' + fullname)
    help.log_to_dialog(message, "plasminka")
    bot.send_message(
        message.chat.id, 'Мінка по формулах з предмету "Фізика плазми."')
    plasminka(message)

def plasminka(message):
    if message.text == 'Хватє':
        key_rem = telebot.types.ReplyKeyboardRemove()
        bot.send_message(
            message.chat.id, 'Окей, удачі на мінці!', reply_markup=key_rem)
    else:
        reply = key.minka_key()
        que = minka.get_plasma_question()
        bot.send_message(message.chat.id, que, reply_markup=reply)
        bot.register_next_step_handler(message, plasminka)

@bot.message_handler(commands=['edminka'])
def edminka_start(message):
    fullname = help.get_fullname(message)
    print('"edminka" command has been used by ' + fullname)
    help.log_to_dialog(message, "edminka")
    msg = bot.send_message(
        message.chat.id,
        "Мінка до екзамену з електродинаміки.\n\nСписок питань підготувала @cassini22."
    )
    edminka(msg)

def edminka(message):
    if message.text == 'Хватє':
        key_rem = telebot.types.ReplyKeyboardRemove()
        bot.send_message(
            message.chat.id, 'Окей, удачі на мінці!', reply_markup=key_rem)
        bot.send_sticker(message.chat.id, 'CAADAgADhwADrKqGF2eV6us-DDCBFgQ')
    else:
        reply = key.minka_key()
        que = minka.get_eldyn_question()
        bot.send_message(message.chat.id, que, reply_markup=reply, parse_mode="Markdown")
        bot.register_next_step_handler(message, edminka)

@bot.message_handler(commands=['exams'])
def exams_start(message):
    fullname = help.get_fullname(message)
    print('"exams" command has been used by ' + fullname)
    help.log_to_dialog(message, "exams")
    rep_key = key.stud_years()
    bot.send_message(
        message.chat.id,
        'Розклад екзаменаційної сесії.\nБудь ласка, оберіть курс.',
        reply_markup=rep_key
    )
    bot.register_next_step_handler(message, exams)

def exams(message):
    if message.text not in c.stud_years:
        rep_key = key.stud_years()
        bot.send_message(
            message.chat.id,
            'Будь ласка, оберіть варіант зі списку.',
            reply_markup=rep_key
        )
        bot.register_next_step_handler(message, exams)
    else:
        with open(exams_sch_path + message.text + '.pdf', 'rb') as file:
            bot.send_document(message.chat.id, file)
        key_rem = telebot.types.ReplyKeyboardRemove()
        bot.send_message(
            message.chat.id,
            '*Увага!*\nДаний розклад був актуальним на 09.12.2019р.\nРозклад може мінятися. Слідкуйте за дошкою оголошень навпроти деканату.',
            reply_markup=key_rem,
            parse_mode="Markdown"
            )

# ADMIN COMMANDS

@bot.message_handler(commands=['getstid'])
def getstid(message):
    bot.send_message(message.chat.id, "Окей, надішліть файл.")
    bot.register_next_step_handler(message, getsticid)


def getsticid(message):
    bot.send_message(message.chat.id, message.sticker.file_id)


@bot.message_handler(commands=['regusers'])
def reg_users(message):
    names = data.registrated_users()
    strnames = ""
    for name in names:
        strnames += name[0]
        strnames += '\n'
    bot.send_message(
        message.chat.id,
        strnames
    )


@bot.message_handler(commands=['setnumerator'])
def setnumerator(message):
    data.set_numerator()
    bot.send_message(message.chat.id, "Зроблено! Тепер - чисельник.")


@bot.message_handler(commands=['setdenominator'])
def setdenominator(message):
    data.set_denominator()
    bot.send_message(message.chat.id, "Зроблено! Тепер - знаменник.")


@bot.message_handler(commands=['howmany'])
def howmany(message):
    data = database.SQL(database_name)
    n = data.count_rows('users')
    data.close()
    bot.send_message(
        message.chat.id, "З ботом контактували " + str(n) + " юзерів.")


@bot.message_handler(commands=['chat_id'])
def het_chat_id(message):
    bot.send_message(message.chat.id, str(message.chat.id))
