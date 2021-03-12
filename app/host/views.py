import os

from django.shortcuts import render, redirect
from django.contrib import messages

from account.decorators import allowed_users

from .forms import HostUpdateForm, EventCreateForm
from .models import Event

# Create your views here.


@allowed_users(['admin'])
def dashboard(request):
    pic_url = request.user.get_prof_pic_url()
    context = {
        'pic_url': pic_url,
    }
    return render(request, 'host/dashboard.html', context=context)


@allowed_users(['admin'])
def profile(request):
    pic_url = request.user.get_prof_pic_url()
    form = HostUpdateForm(instance=request.user)

    if request.POST:
        form = HostUpdateForm(request.POST, request.FILES,
                              instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile Successfully Updated.')
            return redirect('host:dashboard')

    context = {
        'pic_url': pic_url,
        'type': 'Admin',
        'form': form,
        'ipinfo_token': os.environ.get('IPLOOKUP_TOKEN'),
    }
    return render(request, 'prof_update.html', context)


def create_event(request):
    form = EventCreateForm()

    if request.POST:
        form = EventCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)

    context = {
        'form': form
    }

    return render(request, 'host/create_event.html', context=context)


def events(request):
    objects = Event.objects.all()

    context = {
        'events': objects
    }

    return render(request, 'host/events.html', context)


def event_details(request, pk):
    event = Event.objects.get(pk=pk)
    teamData = {}
    try:
        teams = event.registeredteam_set.all()

        for team in teams:
            teamData[team] = team.registeredplayer_set.all()
    except Exception as e:
        print(e)

    context = {
        'event': event,
        'teamData': teamData
    }

    return render(request, 'host/event.html', context)
