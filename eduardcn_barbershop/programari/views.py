from django.shortcuts import render
from django.contrib import messages
from .useful_things import next_2_weeks
from .models import Programare, DetaliiZi
from .forms import ProgramareForm


def index(request):
    return render(request, 'programari/index.html', {'next_2_weeks': next_2_weeks()})


def admin(request):
    return render(request, 'programari/admin.html')

def make_programare(request, date):
    # de fiecare data cand deschidem un link
    # al unei dati calendaristice, verifica daca
    # pentru acea data am definit numarul maxim de programari,
    # timpul de deschidere / inchidere
    if DetaliiZi.objects.filter(data = date).count() == 0:
        ziua_curenta = DetaliiZi(data = date)
        ziua_curenta.save()
    max_programari = DetaliiZi.objects.filter(data = date)[0].max_programari
    programari_zi = Programare.objects.filter(data = date).count()
    programari_ramase = max_programari - programari_zi
    nume = ""
    numar = ""
    ora_programare = ""
    check = 0
    if request.method == "POST" and programari_ramase > 0:
        form = ProgramareForm(request.POST)
        if form.is_valid():
            nume = form.cleaned_data['nume']
            numar = str(form.cleaned_data['numar'])
            ora_programare = form.cleaned_data['ora_programare']
            adauga_programare = Programare(data = date, nume = nume, telefon = numar, ora_programare = ora_programare)
        if not Programare.objects.filter(data = date, ora_programare = ora_programare):
            if not Programare.objects.filter(data = date, telefon = numar):
                adauga_programare.save()
                programari_zi = Programare.objects.filter(data = date).count()
            else:
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
            return render(request, 'programari/success.html', {
                'programari': Programare.objects.filter(data = date, nume = nume, telefon = numar, ora_programare = ora_programare),
                })
    else:
        form = ProgramareForm()

    return render(request, 'programari/programari.html', {'date': [date, next_2_weeks(date)],
                    'programari': Programare.objects.filter(data = date),
                    'programari_ramase': programari_ramase,
                    'form': form,
                    })
