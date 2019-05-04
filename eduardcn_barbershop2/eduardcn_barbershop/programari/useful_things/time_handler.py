from datetime import datetime, timedelta


def get_next_2_weeks():
    days_list = list()
    for day in range(0, 15):
        day = datetime.now() + timedelta(days=day)
        days_list.append(tuple(day.strftime("%d-%m-%Y,%A").split(',')))
    return tuple(days_list)


def convert_days_to_ro(day):
    days = { 'Monday': 'Luni',
             'Tuesday': 'Marti',
             'Wednesday': 'Miercuri',
             'Thursday': 'Joi',
             'Friday': 'Vineri',
             'Saturday': 'Sambata',
             'Sunday': 'Duminica',
             }
    return days.get(day, None)


def get_hours(hour_undefined, nmb_hours):
    hour = datetime.strptime(hour_undefined, '%H:%M')
    output_hours = list()
    cnt = 0
    while cnt < nmb_hours:
        time_to_append = hour + timedelta(minutes=cnt*45)
        output_hours.append(time_to_append.strftime('%H:%M'))
        cnt += 1
    return output_hours