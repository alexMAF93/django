def next_2_weeks(date = ""):
    from datetime import datetime, timedelta
    week_days = {
            'Monday': 'Luni',
            'Tuesday': 'Marti',
            'Wednesday': 'Miercuri',
            'Thursday': 'Joi',
            'Friday': 'Vineri',
            'Saturday': 'Sambata',
            'Sunday': 'Duminica'
    }
    current_day = datetime.today().strftime('%d-%m-%Y')
    next_2_weeks = {}
    for i in range(0, 15):
        some_day = datetime.now() + timedelta(days=i)
        next_2_weeks[some_day.strftime('%d-%m-%Y')] = week_days[some_day.strftime('%A')]
    if date != "":
        return next_2_weeks[date]
    return next_2_weeks


def time_choices(date):
    from .models import DetaliiZi
    TIME_CHOICES = []
    time_choices = []
    for i in range(DetaliiZi.objects.filter(data = date)[0].start_time, DetaliiZi.objects.filter(data = date)[0].end_time):
        if len(str(i)) > 1:
            TIME_CHOICES.append(str(i) + ':00')
        else:
            TIME_CHOICES.append('0' + str(i) + ':00')

    return tuple(TIME_CHOICES)
