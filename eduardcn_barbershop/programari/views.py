from django.shortcuts import render, redirect
from django.contrib import messages
from .useful_things import next_2_weeks, time_choices
from .models import Programare, DetaliiZi
from .forms import ProgramareForm
from django.contrib.auth.decorators import login_required


def index(request):
    # verificam daca avem toate zilele din urmatoarele
    # doua saptamani in baza de date
    for day in next_2_weeks():
        if DetaliiZi.objects.filter(data = day).count() == 0:
            ziua_curenta = DetaliiZi(data = day)
            ziua_curenta.save()

    # stergem zilele vechi din baza de date
    for object in DetaliiZi.objects.all():
        if object.data not in next_2_weeks():
            de_sters = DetaliiZi.objects.filter(data = object.data)
            de_sters.delete()

    FILE = '/home/alex/test_area/django/eduardcn_barbershop/eduardcn_barbershop/istoric.csv'
    for object in Programare.objects.all():
        if object.data not in next_2_weeks():
            with open(FILE, 'a') as f:
                f.write(str(object.data).ljust(15) + ','
                    + str(object.nume).ljust(30) + ','
                    + str(object.telefon).ljust(15) + ','
                    + str(object.ora_programare) + '\n')
                object.delete()
    from django.template.defaulttags import register


    @register.filter
    def get_item(dictionary, key):
        return dictionary.get(key)


    programari_ramase = {}
    for object in DetaliiZi.objects.all():
        max_programari = object.max_programari
        programari_facute = Programare.objects.filter(data = object.data).count()
        programari_ramase[object.data] = max_programari - programari_facute
    return render(request, 'programari/index.html', {'next_2_weeks': next_2_weeks(), 'programari_ramase': programari_ramase})


@login_required
def admin(request):
    options = ['-pastreaza-']
    options.extend([hour for hour in range(8, 22)])
    options2 = ['-pastreaza-']
    options2.extend([hour for hour in range(21, 8, -1)])
    message = ""
    if request.method == "POST":
        if 'modifica_zi' in request.POST:
            data = str(request.POST['data'])
            start_time = str(request.POST['start_time'])
            end_time = str(request.POST['end_time'])
            max_programari = str(request.POST['max_programari'])
            if data != "":
                modificare = DetaliiZi.objects.filter(data = data)[0]
                if start_time != '-pastreaza-':
                    modificare.start_time = start_time
                else:
                    start_time = DetaliiZi.objects.filter(data = data)[0].start_time
                if end_time != '-pastreaza-':
                    modificare.end_time = end_time
                else:
                    end_time = DetaliiZi.objects.filter(data = data)[0].end_time
                if max_programari.isdigit() and max_programari != "":
                    modificare.max_programari = max_programari
                    modificare.save()
                    message = "Modificari realizate cu succes! In data de {}, programarile incep la ora {} si se termina la ora {}. Numarul maxim de programari pentru aceasta zi este:{}.".format(data, start_time, end_time, max_programari)
                else:
                    message = "Trebuie sa scrii un numar pentru numarul maxim de tunsuri dintr-o zi!"
                    return render(request, 'programari/admin.html', {'DetaliiZi': DetaliiZi.objects.all(), 'options1': options,
                                                                        'options2': options2,
                                                                        'message': message,
                                                                        })
        elif 'cauta_programare' in request.POST:
            if Programare.objects.filter(telefon = str(request.POST['numar_telefon'])).count() == 0:
                message = "Nu exista nicio programare pentru acest numar de telefon: {}".format(str(request.POST['numar_telefon']))
            elif str(request.POST['numar_telefon']).isdigit():
                return render(request, 'programari/admin.html',
                    {'DetaliiZi': DetaliiZi.objects.all(), 'options1': options,
                                                           'options2': options2,
                    'detalii': Programare.objects.filter(telefon = str(request.POST['numar_telefon']))})
            else:
                message = "Trebuie sa introduci un numar valid"
        elif 'sterge' in request.POST:
            msg = ""
            for item in request.POST.getlist('content-sters', []):
                data_de_sters = item.split('%')[0]
                telefon_de_sters = item.split('%')[1]
                de_sters = Programare.objects.filter(data = data_de_sters, telefon = telefon_de_sters)
                msg = "Programarea pentru numarul de telefon {} din data de {} a fost stearsa cu success".format(telefon_de_sters, data_de_sters)
                de_sters.delete()
                message += msg
        elif 'modificare_ora' in request.POST:
            msg = ""
            for item in request.POST.getlist('modifica_ora'):
                data_modificare = item.split('%')[0]
                telefon_modificare = item.split('%')[1]
                ora_modificare = item.split('%')[2]
                interval_modificare = time_choices(data_modificare)
                de_modificat = Programare.objects.filter(data = data_modificare, telefon = telefon_modificare)[0]
                if len(ora_modificare) == 1:
                    ora_modificare_formatata = '0' + ora_modificare + ':00'
                elif len(ora_modificare) == 2:
                    ora_modificare_formatata = ora_modificare + ':00'
                else:
                    ora_modificare_formatata = ora_modificare
                if ora_modificare != ora_modificare_formatata:
                    if Programare.objects.filter(data = data_modificare, ora_programare = ora_modificare).count() == 0 and ora_modificare_formatata in interval_modificare:
                        de_modificat.ora_programare = ora_modificare_formatata
                        de_modificat.save()
                        msg = "Modificare realizata cu success. Programarea pentru numarul {} din data de {} este la ora {}".format(telefon_modificare, data_modificare, ora_modificare_formatata)
                    elif ora_modificare_formatata not in interval_modificare:
                        msg = "Doar la aceste ore poti programare in data de {} : {}".format(data_modificare, interval_modificare)
                    else:
                        msg = "Exista deja o programare pentru ora {}".format(ora_modificare)
                    message += msg
    return render(request, 'programari/admin.html', {'DetaliiZi': DetaliiZi.objects.all(), 'options1': options,
                                                        'options2': options2,
                                                        'message': message,
                                                        })


def make_programare(request, date):
    max_programari = DetaliiZi.objects.filter(data = date)[0].max_programari
    programari_zi = Programare.objects.filter(data = date).count()
    ore_luate = []
    for object in Programare.objects.filter(data = date):
        ore_luate.append(object.ora_programare)
    ore_disponibile = []
    for ora in time_choices(date):
        if ora not in ore_luate:
            ore_disponibile.append(ora)
    programari_ramase = max_programari - programari_zi
    nume = ""
    numar = ""
    ora_programare = ""
    check = 0
    if request.method == "POST" and programari_ramase > 0:
        numar = str(request.POST['numar'])
        nume = str(request.POST['nume'])
        ora_programare = str(request.POST['ora_programare'])
        adauga_programare = Programare(data = date, nume = nume, telefon = numar, ora_programare = ora_programare)
        if not Programare.objects.filter(data = date, ora_programare = ora_programare):
            if  Programare.objects.filter(data = date, telefon = numar):
                check = 1
        else:
            check = 2

        if not numar.isdigit() or len(numar) != 10:
            check = 3

        if check == 1:
            messages.error(request, 'Ai deja o programare pentru {}!'.format(date))
        elif check ==2:
            messages.error(request, 'Exista deja o programare la acea ora!')
        elif check == 3:
            messages.error(request, 'Numarul de telefon nu este valid!')
        else:
            adauga_programare.save()
            return render(request, 'programari/success.html', {
                'programari': Programare.objects.filter(data = date, nume = nume, telefon = numar, ora_programare = ora_programare),
                })

    return render(request, 'programari/programari.html', {'date': [date, next_2_weeks(date)],
                    'programari': Programare.objects.filter(data = date),
                    'optiuni': ore_disponibile,
                    'programari_ramase': programari_ramase,
                    })


@login_required
def istoric(request):
    FILE = '/home/alex/test_area/django/eduardcn_barbershop/eduardcn_barbershop/istoric.csv'
    f = open(FILE, 'r')
    content = f.readlines()
    f.close()
    return render(request, 'programari/istoric.html', {'content': content})


def cauta_programare(request):
    rezultat = []
    mesaj = ""
    if request.method == "POST":
        numar_telefon = str(request.POST['cauta-telefon'])
        for object in Programare.objects.filter(telefon = numar_telefon):
            rezultat.append('Programare pe data de {} pentru {} la ora {}'.format(object.data, object.nume, object.ora_programare))

        if len(rezultat) == 0:
            mesaj = "Nu au fost gasite programari pentru numarul {}".format(object.telefon)
        elif len(rezultat) == 1:
            mesaj = "Exista o programare pentru numarul {}:".format(object.telefon)
        else:
            mesaj = "Exista {} programari pentru numarul {}:".format(len(rezultat), object.telefon)


    return render(request, 'programari/cauta_programare.html', {'rezultat': rezultat, 'mesaj': mesaj, })
