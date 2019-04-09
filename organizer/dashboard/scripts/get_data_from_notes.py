#!/usr/bin/env python3


import gkeepapi
import re
from datetime import datetime


def replace_zero(string):
    if len(string) <= 2:
        return re.sub('0[0-9]', string[-1], string)
    else:
        return string


def get_amount_spent(date='', PINNED=True):
    current_date = date
    if not current_date:
        for L in 'dmy':
            data_object = datetime.now().strftime('%' + L)
            if L is 'd' or L is 'm':
                current_date += replace_zero(data_object) + '.'
            else:
                current_date += data_object


    keep = gkeepapi.Keep()
    keep.login('mitroi.alex93@gmail.com', 'dmxbojrmzkbdtose')
    gnote = keep.find(labels=[keep.findLabel('Situatie financiara')])


    for note in gnote:
        if note.pinned == PINNED:
            ID = note.id
            break
    else:
        return [{}, 'Cannot find a pinned note in this label: Situatie financiara!']


    CUMPARATURI = {}
    errors = []
    for text in keep.get(ID).text.split('\n'):
        if text and re.match('\d{1,2}\.\d{1,2}\.\d{2}', text):
            PURCHASES = []
            KEY = text
        elif text and text.startswith('-'):
            PURCHASES.append(text.replace('-', '').split(':'))
        elif text and text.startswith('T:'):
            CUMPARATURI[KEY] = PURCHASES
        else:
            if not CUMPARATURI.get(KEY, None):
                CUMPARATURI[KEY] = PURCHASES
    TOTAL = 0
    for intrari in CUMPARATURI.get(current_date, 'nothing'):
        try:
            TOTAL += float(intrari[-1])
        except ValueError:
            errors.append('Cannot retrieve purchases for this date!')
            break

    return [CUMPARATURI.get(current_date, 'Nothing'), TOTAL, errors]
