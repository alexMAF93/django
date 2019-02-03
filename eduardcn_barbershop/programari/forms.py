from django import forms


class ProgramareForm(forms.Form):
    from .useful_things import time_choices
    nume = forms.CharField(label = 'Nume:', required = True)
    numar = forms.CharField(label = 'Telefon', required = True)
    #ora_programare = forms.ChoiceField(choices = time_choices())
