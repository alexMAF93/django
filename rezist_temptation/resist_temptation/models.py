from django.db import models

# Create your models here.

class Temptation(models.Model):
    temptation = models.CharField(max_length=255)
    added_time = models.DateField()
    resisted_count = models.IntegerField(default=0)
    gave_in_count = models.IntegerField(default=0)
    username=models.CharField(max_length=255, default='admin')