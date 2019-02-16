from django.db import models


class Programare(models.Model):
    class Meta:
        ordering =[
            'data',
            'ora_programare',
        ]
    data = models.CharField(max_length = 10)
    nume = models.CharField(max_length = 50)
    telefon = models.CharField(max_length = 10, default = '0')
    ora_programare = models.CharField(null = True, max_length = 5)


class DetaliiZi(models.Model):
    data = models.CharField(max_length = 10, unique = True)
    max_programari = models.IntegerField(default = 0)
    start_time = models.IntegerField(default = 11)
    end_time = models.IntegerField(default = 21)
