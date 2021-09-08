from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Temptation, GoodHabit
import datetime
import plotly.graph_objs as go


# @login_required

def index(request):
    return render(request, 'resist_temptation/index.html', {'date': datetime.date.today()})


def good_habits(request):
    today = datetime.date.today()
    return_dict = {'habits': [], 'date': today}

    if request.method == "POST":
        if 'add_habit' in request.POST:
            habit = str(request.POST['habit'])
            habit_to_add = GoodHabit(added_time=today,
                                            habit=habit,
                                                )
            habit_to_add.save()
        elif 'increase' in request.POST:
            habit_to_increase = GoodHabit.objects.filter(habit=request.POST['increase'], added_time=today)[0]
            performed_count = habit_to_increase.performed_count + 1 if habit_to_increase.performed_count + 1 > 0 else 1
            habit_to_increase.performed_count = performed_count
            habit_to_increase.save()
        elif 'delete' in request.POST:
            habits_to_ignore = GoodHabit.objects.filter(habit=request.POST['delete'])
            for habit in habits_to_ignore:
                habit.ignore = True
                habit.save() 


    todays_habits = GoodHabit.objects.filter(added_time=today, ignore=False)
    if len(todays_habits) == 0:
        yesterday = today - datetime.timedelta(days=1)
        for habit in GoodHabit.objects.filter(added_time=yesterday, ignore=False):
            habit_to_add = GoodHabit(added_time=today,
                                            habit=habit.habit,
                                                )
            habit_to_add.save()
    return_dict['habits'] = GoodHabit.objects.filter(added_time=today, ignore=False)

    return render(request, 'resist_temptation/good_habits.html', return_dict)


def temptations(request):
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
        elif 'delete' in request.POST:
            temptations_to_ignore = Temptation.objects.filter(temptation=request.POST['delete'])
            for temptation in temptations_to_ignore:
                temptation.ignore = True
                temptation.save() 


    todays_temptations = Temptation.objects.filter(added_time=today, ignore=False)
    if len(todays_temptations) == 0:
        yesterday = today - datetime.timedelta(days=1)
        for temptation in Temptation.objects.filter(added_time=yesterday, ignore=False):
            temptation_to_add = Temptation(added_time=today,
                                            temptation=temptation.temptation,
                                            resisted_count=0,
                                            gave_in_count=0
                                                )
            temptation_to_add.save()
    return_dict['temptations'] = Temptation.objects.filter(added_time=today, ignore=False)

    return render(request, 'resist_temptation/temptations.html', return_dict)


def temptations_statistics(request):
    return_dict = dict()
    temptations = Temptation.objects.order_by().values('temptation').distinct()
    return_dict['plot_div'] = []
    for temptation in temptations:
        x_data = [x.added_time for x in Temptation.objects.filter(temptation=temptation['temptation'])[:10]]
        y1_data = [x.gave_in_count for x in Temptation.objects.filter(temptation=temptation['temptation'])[:10]]
        y2_data = [x.resisted_count for x in Temptation.objects.filter(temptation=temptation['temptation'])[:10]]
        max_range = max(y1_data) if max(y1_data) > max(y2_data) else max(y2_data)
        min_range = -1 * max_range
        layout = go.Layout(title=temptation['temptation'], dragmode=False, yaxis={'range': [min_range-2, max_range+2]})
        plot_div = go.Figure(data=[go.Bar(x=x_data, y=y1_data,
                            name='gave in',
                            opacity=0.8, marker_color='red', showlegend=True),
                            go.Bar(x=x_data, y=y2_data,
                                name='resisted',
                                opacity=0.8, marker_color='green', showlegend=True)], 
                            layout=layout, ).to_html()
        return_dict['plot_div'].append(plot_div)

    return render(request, 'resist_temptation/temptation_statistics.html', return_dict)


def good_habits_statistics(request):
    return_dict = dict()
    habits = GoodHabit.objects.order_by().values('habit').distinct()
    return_dict['plot_div'] = []
    for habit in habits:
        x_data = [x.added_time for x in GoodHabit.objects.filter(habit=habit['habit'])[:10]]
        y_data = [x.performed_count for x in GoodHabit.objects.filter(habit=habit['habit'])[:10]]
        max_range = max(y_data) + 1 if max(y_data) > 0 else 2
        min_range = -1 * max_range
        layout = go.Layout(title=habit['habit'], dragmode=False, yaxis={'range': [min_range, max_range]})
        plot_div = go.Figure(data=[go.Bar(x=x_data, y=y_data,
                            name='performed count',
                            opacity=0.8,  showlegend=True),
                            ], 
                            layout=layout, ).to_html()
        return_dict['plot_div'].append(plot_div)
    return render(request, 'resist_temptation/good_habits_statistics.html', return_dict)
