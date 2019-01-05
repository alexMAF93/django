#!/usr/local/bin/python3


def get_credentials_for_email(PASSWD_FILE):
    with open(PASSWD_FILE, 'r') as f:
        return f.read().split(' ')
