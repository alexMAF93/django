from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.views import generic
from .forms import SignUpForm


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            email_address = form.cleaned_data.get('email')
            user = authenticate(username = username, email = email_address, password = raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


def show_profile(request):
    return render(request, 'accounts/profile.html')
