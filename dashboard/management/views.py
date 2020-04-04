from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.


def index(request):
    return_dict = {'message': 'This is a test.'}

    return render(request, 'programari/index.html', return_dict)
