from django.shortcuts import render
from .useful_things.time_handler import get_next_2_weeks, convert_days_to_ro, get_hours
from .models import DayDetails, Appointment
from django.contrib.auth.decorators import login_required


def index(request):
    return_dict = dict()
    days = []
    next_2_weeks = [i[0] for i in get_next_2_weeks()]
    for day in get_next_2_weeks():
        if DayDetails.objects.filter(date=day[0]).count() == 0:
            add_day = DayDetails(date=day[0])
            add_day.save()
        day_in_ro = convert_days_to_ro(day[1])
        append_max_spots = DayDetails.objects.filter(date=day[0])[0].max_appointments
        append_free_spots = append_max_spots - Appointment.objects.filter(date=day[0]).count()
        days.append((day[0], day_in_ro, append_free_spots, append_max_spots))

    return_dict['days'] = days

    # cleaning the days that passed
    for day in DayDetails.objects.all():
        if not day.date in next_2_weeks:
            DayDetails.objects.filter(date=day.date)[0].delete()

    return render(request, 'programari/index.html', return_dict)


def make_appointment(request, date, day):
    return_dict = dict()
    return_dict['date'] = date
    return_dict['day'] = day
    return_dict['message'] = list()
    return_dict['appointment_time'] = list()
    appointment_day = DayDetails.objects.filter(date=date)[0]
    hours_taken = list()


    if request.method == "POST":
        print(request.POST)
        if 'create_appointment' in request.POST:
            name = str(request.POST['name'])
            phone = str(request.POST['phone'])
            appointment_time = str(request.POST['appointment_time'])

            # the name field can contain any value
            if not name:
                return_dict['message'].append('Trebuie sa-ti scrii numele')

            # the phone field must contain a valid phone number
            if phone:
                if phone[0] == '0' and len(phone) == 10:
                    for character in phone:
                        if not character.isdigit():
                            return_dict['message'].append('Numarul de telefon trebuie sa contina doar cifre.')
                            break
                    if len(Appointment.objects.filter(date=date, phone=phone)) > 0:
                        return_dict['message'].append('Exista deja o programare pentru acest numar de telefon in aceasta data.')
                else:
                    return_dict['message'].append('Numarul de telefon trebuie sa inceapa cu 0 si sa contina 10 cifre.')
            else:
                return_dict['message'].append('Trebuie sa-ti scrii numarul de telefon.')

            # appointment_time should be ok, so nothing to check here
            if len(return_dict['message']) == 0:
                appointment_to_add = Appointment(date=date,
                                                 name=name,
                                                 phone=phone,
                                                 appointment_time=appointment_time
                                                 )
                appointment_to_add.save()
                return_dict['name'] = name
                return_dict['phone'] = phone
                return_dict['appointment_time'] = appointment_time
                return render(request, 'programari/success.html', return_dict)

        check_modify = 0
        for key in request.POST:
            if 'delete_appointment' in key:
                check_modify = 1
            elif 'edit_appointment' in key:
                check_modify = 2
        if check_modify == 1:
            for phone_delete in request.POST.getlist('to_modify', []):
                if len(phone_delete) == 10:
                    to_be_deleted = Appointment.objects.filter(date=date, phone=phone_delete)[0]
                    to_be_deleted.delete()
                    return_dict['message'].append('Programarea pentru {} a fost stearsa.'.format(phone_delete))
        elif check_modify == 2:
            appointment_time = str(request.POST['appointment_time']).split('%')[0]
            old_time = str(request.POST['appointment_time']).split('%')[1]
            to_be_modified = Appointment.objects.filter(date=date, appointment_time=old_time)[0]
            if Appointment.objects.filter(date=date, appointment_time=appointment_time).count() == 0:
                to_be_modified.appointment_time = appointment_time
                to_be_modified.save()
                return_dict['message'].append('Programarea lui {} a fost mutata la ora {}.'.format(
                                            to_be_modified.name,
                                            to_be_modified.appointment_time
                ))
                print(return_dict['message'])
            else:
                return_dict['message'].append('Exista deja o programare la ora {}'.format(appointment_time))
    return_dict['appointments'] = list()
    for appointment in Appointment.objects.filter(date=date):
        return_dict['appointments'].append((
                appointment.name,
                appointment.phone,
                appointment.appointment_time
            ))
    for appointment in Appointment.objects.filter(date=date):
        hours_taken.append(appointment.appointment_time)
    available_hours= get_hours(appointment_day.start_time,
                                appointment_day.max_appointments)
    for hour in available_hours:
        if not hour in hours_taken:
            return_dict['appointment_time'].append(hour)
    return render(request, 'programari/make_appointment.html', return_dict)


@login_required
def admin_page(request):
    return_dict = dict()
    return_dict['message'] = []
    available_days = list()

    # the list of days that can be modified
    for day in get_next_2_weeks():
        available_days.append((day[0], convert_days_to_ro(day[1])))
    return_dict['available_days'] = available_days

    # if the submit button was pressed
    if request.method == "POST":
        # change the specs of a day
        if 'modify_day' in request.POST:
            date_to_modify = str(request.POST['day_to_modify'])
            start_time = str(request.POST['start_time'])
            max_appointments = str(request.POST['max_appointments'])

            # we must make sure that start time is a number
            # and that it's not bigger than 22
            if start_time:
                if len(start_time) <= 2:
                    try:
                        a = int(start_time)
                        print('a=',a)
                    except:
                        return_dict['message'].append('Ora de inceput nu este valida')
                    else:
                        if a <= 22 and a >= 7:
                            start_time = '0' + str(a) + ':00'
                            if len(start_time) > 5:
                                start_time = start_time[1:]
                        else:
                            return_dict['message'].append('Poti face programari doar in intervalul orar 7, 22')
                else:
                    try:
                        a = int(start_time.split(':')[0])
                        if a < 7 or a > 22:
                            return_dict['message'].append('Poti face programari doar in intervalul orar 7, 22')
                        else:
                            if len(start_time.split(':')[0]) < 2:
                                start_time = '0' + start_time
                    except:
                        return_dict['message'].append('Ora introdusa nu este valida')
            elif max_appointments == '0':
                to_be_deleted = DayDetails.objects.filter(date=date_to_modify)[0]
                to_be_deleted.start_time = ""
                to_be_deleted.max_appointments = 0
                to_be_deleted.save()
                return_dict['message'].append('Nu se mai pot face programari in data de {}'.format(
                                                date_to_modify
                ))
                for appointment in Appointment.objects.filter(date=date_to_modify):
                    return_dict['message'].append('Programarea lui {} - {} de la ora {} a fost stearsa'.format(
                                            appointment.name,
                                            appointment.phone,
                                            appointment.appointment_time
                    ))
                    appointment.delete()
            else:
                try:
                    start_time = DayDetails.objects.filter(date=date_to_modify)[0].start_time
                except:
                    return_dict['message'].append('Trebuie sa introduci ora de inceput.')

            # the minimum number of appointments is 1
            if max_appointments:
                if start_time:
                    try:
                        max_appointments = int(max_appointments)
                    except:
                        return_dict['message'].append('Trebuie sa introduci numarul de programari pentru aceasta zi')
                    if max_appointments <= 0:
                        return_dict['message'].append('Numarul de programari trebuie sa fie mai mare ca 0')
            else:
                return_dict['message'].append('Trebuie sa introduci numarul de programari pentru aceasta zi')

            # if everything is ok, we move on
            if len(return_dict['message']) == 0:
                return_dict['message'].append('Modificari realizate cu succes.')
                return_dict['message'].append('In data de {}, programarile incep de la ora {}'.format(date_to_modify, start_time))
                return_dict['message'].append('Numarul maxim de programari este: {}'.format(max_appointments))
                day_to_modify = DayDetails.objects.filter(date=date_to_modify)[0]
                day_to_modify.start_time = start_time
                day_to_modify.max_appointments = max_appointments
                day_to_modify.save()

        elif 'search_appointment' in request.POST:
            phone = request.POST['phone']
            return_dict['appointments'] = list()
            if Appointment.objects.filter(phone=phone).count() > 0:
                for appointment in Appointment.objects.filter(phone=phone):
                    return_dict['appointments'].append((appointment.date,
                                                       appointment.name,
                                                       appointment.phone,
                                                       appointment.appointment_time))
                return render(request, 'programari/search.html', return_dict)
            else:
                return_dict['message'].append('Nu a fost gasita o programare pentru numarul {}'.format(
                    phone
                ))
        elif 'delete_appointment' in request.POST:
            for to_be_deleted in request.POST.getlist('to_delete', []):
                date = to_be_deleted.split('%')[0]
                phone = to_be_deleted.split('%')[1]
                delete_appointment = Appointment.objects.filter(date=date, phone=phone)
                delete_appointment.delete()
                return_dict['message'].append('Programarea pentru numarul {} stearsa pentru data de {}'.format(
                                                        phone,
                                                        date
                ))

    return render(request, 'programari/admin.html', return_dict)