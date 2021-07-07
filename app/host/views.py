import os

from django.shortcuts import render, redirect
from django.contrib import messages

from account.decorators import allowed_users

from .forms import HostUpdateForm, EventCreateForm, CategoryCreateForm
from .models import Event, Category

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


def create_event(request):
    form = EventCreateForm()

    if request.POST:
        form = EventCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('host:events')
        else:
            print(form.errors)

    context = {
        'form': form,
        'mode': 'Create'
    }

    return render(request, 'host/create_event.html', context=context)


def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    form = EventCreateForm(instance=event)

    if request.POST:
        form = EventCreateForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)

    context = {
        'form': form,
        'mode': 'Update',
    }

    return render(request, 'host/create_event.html', context=context)


def delete_event(request, event_id):
    Event.objects.get(pk=event_id).delete()
    return redirect('host:events')


def categories(request, event_id):
    event = Event.objects.get(pk=event_id)
    all_categories = event.category_set.all()

    context = {
        'categories': all_categories,
        'event': event,
    }

    return render(request, 'host/categories.html', context=context)


def create_category(request, event_id):
    event = Event.objects.get(pk=event_id)
    form = CategoryCreateForm()

    if request.POST:
        form = CategoryCreateForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.event = event
            c.save()
            return redirect('host:categories', event_id=event_id)
        else:
            print(form.errors)

    context = {
        'form': form,
        'event': event,
        'mode': 'Create'
    }

    return render(request, 'host/create_category.html', context=context)


def update_category(request, event_id, category_id):
    event = Event.objects.get(pk=event_id)
    category = Category.objects.get(pk=category_id)
    form = CategoryCreateForm(instance=category)

    if request.POST:
        form = CategoryCreateForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('host:categories', event_id=event_id)
        else:
            print(form.errors)

    context = {
        'form': form,
        'event': event,
        'mode': 'Update'
    }

    return render(request, 'host/create_category.html', context=context)


def delete_category(request, event_id, category_id):
    event = Event.objects.get(pk=event_id)
    event.category_set.get(pk=category_id).delete()
    return redirect('host:categories', event_id=event_id)
