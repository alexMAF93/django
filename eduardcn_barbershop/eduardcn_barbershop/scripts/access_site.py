#!/usr/local/bin/python3


import requests
from datetime import datetime


r = requests.get('http://localhost:5000')
right_now = datetime.now().strftime('%d, %b %Y %H:%M')
with open('/tmp/site_status.txt', 'a') as f:
    f.write('='*18 + '\n' + "{}\nStatus code:{}\n".format(right_now, r.status_code) + '='*18 + '\n\n')
