# -*- coding: utf-8 -*-

# %%

import os
import random
import pandas as pd

import numpy as np
from openpyxl import load_workbook
mnkDir = 'minka_files/'
ex = os.path.abspath(mnkDir + "Мінка кванти.xlsx")
wb = load_workbook(ex)
cons = wb[wb.sheetnames[0]]

eldynQ = pd.read_csv(mnkDir+'electrodyn.txt', header=None, sep='&')
plasmQ = [
"Середня локальна швидкість",
"Довжина Дебая",
"Потенціал Дебая-Хюккеля",
"Власна частота коливань плазми",
"Гірочастота",
"Ларморівський радіус",
"Адіабатичний інваріант: обертання по колу",
"Адіабатичний інваріант: поздовжній рух",
"Адіабатичний інваріант: рух в напрямку перпендикулярному до напрямку силових ліній магнітного поля",
"Період баунс-коливань(конус втрат)",
"Система рівнянь Максвелла для МГД",
"Р-ня неперервності в МГД",
"Р-ня руху в МГД",
"Р-ня стану адіабати",
"Плазмовий параметр 'бета'",
"Умова вмороженості",
"Рівняння індукції",
]


# %%
def get_qm_question(nsem):
    if nsem == '1 семестр':
        sem = list(np.arange(3,74))
    elif nsem == '2 семестр':
        sem = list(np.arange(75,138))
    else:
        sem = list(np.arange(3,74))+list(np.arange(75,138))
    q = random.choice(sem)
    question =  cons['A'+ str(q)].value + ". " + cons['B'+ str(q)].value
    return(question)

def get_plasma_question():
    question = random.choice(plasmQ)
    return(question)

def get_eldyn_question():
    ind = random.choice(range(len(eldynQ[0])))
    question = "*" + eldynQ[0][ind] + "*\n\n" + eldynQ[1][ind]
    return(question)
