from django.db import models

# Create your models here.


class Appointment(models.Model):
    class Meta:
        ordering =[
            'date',
            'appointment_time',
        ]
    date = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10, default='0')
    appointment_time = models.CharField(null=True, max_length=5)


class DayDetails(models.Model):
    date = models.CharField(max_length=10, unique=True)
    max_appointments = models.IntegerField(default = 0)
    start_time = models.CharField(max_length=5)