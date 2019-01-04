from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SendJokeForm, SubscribeToJokesForm
from .models import Subscribers
from subprocess import Popen, PIPE
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    return render(request, 'board/index.html', {'title': 'Home Page'})


@login_required
def user_profile(request):
    return render(request, 'board/about.html')


@login_required
def apps(request):
    return render(request, 'board/apps.html', {'title': 'My Apps'})


@login_required
def jokes(request):
    email_address = ""
    if request.method == "POST":
        form = SendJokeForm(request.POST)
        if form.is_valid():
            email_address = form.cleaned_data['send_to_email']
            Popen(['board/scripts/jokes.py', email_address])
            messages.success(request, f'A joke was sent to ' + email_address + '!')
            return redirect('jokes')
    else:
        form = SendJokeForm()

    return render(request, 'board/jokes.html', {'title': 'Jokes Through email',
                        'form':form,
                        'email_address':email_address})


@login_required
def subscribe_jokes(request):
    email_address_to_add = ""
    check_email = 0
    number_of_subscribers = Subscribers.objects.count()
    if request.method == "POST":
        form = SubscribeToJokesForm(request.POST)
        if form.is_valid():
            email_address_to_add = form.cleaned_data['subscribe_email']
            if Subscribers.objects.filter(email_address = email_address_to_add):
                check_email = 1
                messages.error(request, 'This email address is already in our database')
            else:
                add_email = Subscribers(email_address_to_add)
                add_email.save()
                number_of_subscribers = Subscribers.objects.count()
                messages.success(request, email_address_to_add + ' is now in our list')
            return render(request, 'board/subscribe_to_jokes.html',
                {'title': 'You just subscribed',
                'form': form,
                'email_address': email_address_to_add,
                'number_of_subscribers': number_of_subscribers,})
    else:
        form = SubscribeToJokesForm()
    return render(request, 'board/subscribe_to_jokes.html',
        {'title': 'Get jokes daily',
        'form': form,
        'number_of_subscribers': number_of_subscribers,})


@login_required
def server_details(request):
    content = ""
    output = Popen(['board/scripts/get_data.py'], stdout = PIPE)
    for bytes in output.stdout:
        line = bytes.decode()
        content += line
    return render(request, 'board/server.html', {'title': 'Server Details',
                                                'content': content})
