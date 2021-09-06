from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Temptation
import datetime


# @login_required
def index(request):
    today = datetime.date.today()
    return_dict = {'temptations': [], 'date': today}

    if request.method == "POST":
        if 'add_temptation' in request.POST:
            temptation = str(request.POST['temptation'])
            temptation_to_add = Temptation(added_time=today,
                                            temptation=temptation,
                                            resisted_count=0,
                                            gave_in_count=0
                                                )
            temptation_to_add.save()
        elif 'increase' in request.POST:
            temptation_to_increase = Temptation.objects.filter(temptation=request.POST['increase'], added_time=today)[0]
            resisted_count = temptation_to_increase.resisted_count + 1
            temptation_to_increase.resisted_count = resisted_count
            temptation_to_increase.save()
        elif 'decrease' in request.POST:
            temptation_to_increase = Temptation.objects.filter(temptation=request.POST['decrease'], added_time=today)[0]
            gave_in_count = temptation_to_increase.gave_in_count + 1
            temptation_to_increase.gave_in_count = gave_in_count
            temptation_to_increase.save()

    todays_temptations = Temptation.objects.filter(added_time=today)
    if len(todays_temptations) == 0:
        yesterday = today - datetime.timedelta(days=1)
        for temptation in Temptation.objects.filter(added_time=yesterday):
            temptation_to_add = Temptation(added_time=today,
                                            temptation=temptation.temptation,
                                            resisted_count=0,
                                            gave_in_count=0
                                                )
            temptation_to_add.save()
    return_dict['temptations'] = Temptation.objects.filter(added_time=today)

    return render(request, 'resist_temptation/index.html', return_dict)
