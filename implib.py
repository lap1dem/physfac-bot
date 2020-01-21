from config import *
import os
import constants as c
import json
from telebot.types import InputMediaPhoto
from datetime import date
import psycopg2 as psql
import shelve as sh
from telebot.types import (
    ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
)
import random
import pandas as pd
import numpy as np
from openpyxl import load_workbook

import modules.navigation as nav

def send_dev_msg(msg):
    bot.send_message(
        msg.chat.id,
        c.dev_msg
    )
