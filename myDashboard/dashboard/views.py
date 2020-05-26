from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def index(request):
    return_dict = {'message': ['Hello,', 'World!']}

    return render(request, 'dashboard/index.html', return_dict)
