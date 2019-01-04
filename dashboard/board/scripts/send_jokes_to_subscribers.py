#!/usr/local/bin/python3


import django
import sys
import os
from subprocess import Popen


sys.path.append(os.path.abspath("/home/alex/test_area/django/dashboard"))
os.environ['DJANGO_SETTINGS_MODULE'] = 'dashboard.settings'
django.setup()


from board.models import Subscribers


emails = ''
for email in Subscribers.objects.all():
    emails = emails + str(email) + ' '


Popen(['/home/alex/test_area/django/dashboard/board/scripts/jokes.py ' + emails], shell = True)
