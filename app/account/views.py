import os
import re
import requests

from django.shortcuts import render, redirect

from django.contrib.auth import login, authenticate

from .forms import TLRegistrationForm

from .models import (
    User,
    TeamLeaderModel,
)

# Create your views here.

envs = dict(os.environ)


def loginView(request):
    return


def sample(request):
    users = User.objects.all()
    pic_urls = list()
    for user in users:
        pic_urls.append(user.get_prof_pic_url())
    print(pic_urls)
    return render(request, 'account/sample.html', context={'pic_urls': pic_urls})


def registration_view(request):
    form = TLRegistrationForm()
    errors = []

    if request.POST:
        form = TLRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            url = 'https://www.google.com/recaptcha/api/siteverify'
            data = {
                'secret': envs.get('OWNER_KEY'),
                'response': request.POST.get('g-recaptcha-response')
            }
            data = requests.post(url, data=data).json()
            if data.get('success'):
                print('Succeed!!')
                form.save()
                email = form.cleaned_data.get('email')
                raw_password = form.cleaned_data.get('password1')
                account = authenticate(email=email, password=raw_password)
                login(request, account)
                return redirect('home:comingsoon')
            else:
                print('Not Succeed!!')
                errors.append('Captcha Not Provided')

    context = {
        'form': form,
        'ipinfo_token': envs.get('IPLOOKUP_TOKEN'),
        'recaptcha_token': envs.get('CLIENT_KEY'),
        'errors': errors,
        'type': 'Team Leader'
    }

    return render(request, 'account/register.html', context)