from django.db import models

# Create your models here.

class Temptation(models.Model):
    temptation = models.CharField(max_length=255)
    added_time = models.DateField()
    resisted_count = models.IntegerField(default=0)
    gave_in_count = models.IntegerField(default=0)
    username=models.CharField(max_length=255, default='admin')
    ignore=models.BooleanField(default=False)

    def __str__(self):
        return "{} {}".format(self.temptation, self.added_time)

    class Meta:
        ordering = ('added_time', 'temptation')


class GoodHabit(models.Model):
    habit = models.CharField(max_length=255)
    added_time = models.DateField()
    performed_count = models.IntegerField(default=-1)
    username=models.CharField(max_length=255, default='admin')
    ignore=models.BooleanField(default=False)

    def __str__(self):
        return "{} {}".format(self.habit, self.added_time)

    class Meta:
        ordering = ('added_time', 'habit')