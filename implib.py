from config import *
import json
import os
import random
import shelve as sh
from datetime import date

import numpy as np
import pandas as pd
import psycopg2 as psql
from openpyxl import load_workbook
from telebot.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           InputMediaPhoto, ReplyKeyboardMarkup)

import constants as c
import modules.navigation as nav


def send_dev_msg(msg):
    bot.send_message(
        msg.chat.id,
        c.dev_msg
    )
