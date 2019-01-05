#!/usr/local/bin/python3


from email.mime.text import MIMEText
from subprocess import PIPE, Popen
import smtplib, urllib.request, re, sys
from useful_functions import get_credentials_for_email as get_creds


def check_if_email(recipients):
    check = 0
    for email in recipients:
        if not '@' in str(email):
            check = 0
        else:
            check+=1
        if check == 0:
            return False
    return True


recipients = sys.argv[1:] # here we will have the email addresses


if not check_if_email(recipients):
    print('ERROR: database does not contain just email addresses!')
    sys.exit(7)


url = "http://www.rinkworks.com/jokes/random.cgi"
joke = urllib.request.urlopen(url).readlines()
check_var = 0
MESSAGE = ""

for i in range(len(joke) - 1):
    if str(joke[i].decode()).startswith('<h2>#'):
        check_var = 1
    if str(joke[i].decode()).startswith('</td>') and check_var == 1:
        break

    if check_var == 1:
         MESSAGE += re.sub('</?..?/?>|<img.*/>', '', str(joke[i].decode()))


msg = MIMEText(MESSAGE)
msg["Subject"] = "Esti cel mai tare!!!"
msg["From"] = "alex"
msg["To"] = "everyone"
ACCOUNT = get_creds('/home/alex/parole/send_email.txt')[0]
PASSWORD = get_creds('/home/alex/parole/send_email.txt')[1].replace('\n', '')


t = smtplib.SMTP("smtp.gmail.com", 587)
t.ehlo()
t.starttls()
t.login(ACCOUNT, PASSWORD)
t.sendmail(ACCOUNT, recipients, msg.as_string())
t.quit()
