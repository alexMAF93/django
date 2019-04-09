from django.shortcuts import render
from subprocess import PIPE, Popen
import os
from .scripts.useful_functions import sort_data
from .scripts.get_data_from_notes import get_amount_spent
from datetime import datetime


def index(request):
    return_dict = {}
    pwd = os.getcwd()
    command = '{}/dashboard/scripts/manga_chapters.py'.format(pwd)
    get_manga = Popen(command.split(), stdout=PIPE, stderr=PIPE)
    (output, errors) = get_manga.communicate()
    mangas = sort_data(output.decode())
    if output:
        return_dict['mangas'] = mangas

    amount_details = get_amount_spent()
    SHOPPINGS = amount_details[0]
    AMOUNT = amount_details[1]
    errors = ''
    try:
        errors = ' '.join(amount_details[2])
    except:
        errors = ''
    if errors:
        return_dict['errors'] = errors
    else:
        if SHOPPINGS:
            return_dict['shoppings'] = []
            for entry in SHOPPINGS:
                return_dict['shoppings'].append(','.join(entry[:-1]) + ':' + entry[-1])
        return_dict['amount'] = AMOUNT
    return_dict['date'] = datetime.now().strftime('%d.%m.%Y')


    return render(request, 'dashboard/index.html',
                  return_dict)

def search_purchase(request):
    pass