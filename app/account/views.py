import os
import re
import requests

from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib.auth import login, authenticate, logout

from .forms import TLRegistrationForm, JudgeRegistrationForm

from .models import User

from .decorators import unauthenticated_user

# Create your views here.

envs = dict(os.environ)


def sample(request):
    users = User.objects.all()
    pic_urls = list()
    for user in users:
        pic_urls.append(user.get_prof_pic_url())
    return render(request, 'account/sample.html', context={'users': users, 'pic_urls': pic_urls})


@unauthenticated_user
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
                messages.success(request, 'Successfully Registered.')
                return redirect('team_leader:dashboard')
            else:
                print('Not Succeed!!')
                errors.append('Captcha Not Provided')

    context = {
        'form': form,
        'ipinfo_token': envs.get('IPLOOKUP_TOKEN'),
        'recaptcha_token': envs.get('CLIENT_KEY'),
        'errors': errors,
        'type': 'Team Admin'
    }

    return render(request, 'account/register.html', context)


@unauthenticated_user
def judge_registration_view(request):
    form = JudgeRegistrationForm()
    errors = []

    if request.POST:
        form = JudgeRegistrationForm(request.POST, request.FILES)
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
                messages.success(request, 'Successfully Registered.')
                return redirect('account:sample')
            else:
                print('Not Succeed!!')
                errors.append('Captcha Not Provided')

    context = {
        'form': form,
        'ipinfo_token': envs.get('IPLOOKUP_TOKEN'),
        'recaptcha_token': envs.get('CLIENT_KEY'),
        'errors': errors,
        'type': 'Judge'
    }

    return render(request, 'account/register.html', context)


@unauthenticated_user
def login_view(request):
    errors = []

    if request.POST:
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully Logged In.')
            next = request.GET.get('next')
            if next:
                return redirect(next)
            elif user.is_tl:
                return redirect('team_leader:dashboard')
            elif user.is_judge:
                return redirect('judge:dashboard')
            else:
                return redirect('account:sample')
        else:
            errors.append('Check E-mail/Password and try again.')

    context = {
        'recaptcha_token': envs.get('CLIENT_KEY'),
        'errors': errors,
    }

    return render(request, 'account/login.html', context=context)


def logout_view(request):
    logout(request)
    return redirect('account:sample')
