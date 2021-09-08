from django.contrib import admin

# Register your models here.

from resist_temptation.models import Temptation, GoodHabit


admin.site.register(Temptation)
admin.site.register(GoodHabit)