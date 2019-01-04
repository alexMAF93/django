from django.db import models


class Subscribers(models.Model):
    def __str__(self):
        return self.email_address


    email_address = models.CharField(max_length = 200, primary_key = True)
