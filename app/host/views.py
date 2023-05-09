import os

from django.shortcuts import render, redirect
from django.contrib import messages

from account.decorators import allowed_users

from .forms import HostUpdateForm, EventCreateForm, CategoryCreateForm, SubCategoryCreateForm
from .models import Event, Category, SubCategory

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


@allowed_users(['admin'])
def events(request):
    objects = Event.objects.all()

    context = {
        'events': objects
    }

    return render(request, 'host/events.html', context)


@allowed_users(['admin'])
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


@allowed_users(['admin'])
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


@allowed_users(['admin'])
def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    form = EventCreateForm(instance=event)

    if request.POST:
        form = EventCreateForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('host:events')
        else:
            print(form.errors)

    context = {
        'form': form,
        'mode': 'Update',
    }

    return render(request, 'host/create_event.html', context=context)


@allowed_users(['admin'])
def delete_event(request, event_id):
    Event.objects.get(pk=event_id).delete()
    return redirect('host:events')


@allowed_users(['admin'])
def categories(request, event_id):
    event = Event.objects.get(pk=event_id)
    all_categories = event.category_set.all()

    context = {
        'categories': all_categories,
        'event': event,
    }

    return render(request, 'host/categories.html', context=context)


@allowed_users(['admin'])
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


@allowed_users(['admin'])
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


@allowed_users(['admin'])
def delete_category(request, event_id, category_id):
    event = Event.objects.get(pk=event_id)
    event.category_set.get(pk=category_id).delete()
    return redirect('host:categories', event_id=event_id)




# Sub Category Section

@allowed_users(['admin'])
def sub_categories(request, event_id, category_id):
    event = Event.objects.get(pk=event_id)
    category = Category.objects.get(pk=category_id)

    all_subcategories = category.subcategory_set.all()

    context = {
        'sub_categories': all_subcategories,
        'category': category,
        'event': event,
    }

    return render(request, 'host/sub_categories.html', context=context)


@allowed_users(['admin'])
def create_subcategory(request, event_id, category_id):
    event = Event.objects.get(pk=event_id)
    catetgory = Category.objects.get(pk=category_id)
    form = SubCategoryCreateForm()

    if request.POST:
        form = SubCategoryCreateForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.category = catetgory
            c.save()
            return redirect('host:sub_categories', event_id=event_id, category_id=category_id)
        else:
            print(form.errors)

    context = {
        'form': form,
        'event': event,
        'category': catetgory,
        'mode': 'Create'
    }

    return render(request, 'host/create_subcategory.html', context=context)


@allowed_users(['admin'])
def update_subcategory(request, event_id, category_id, subcategory_id):
    event = Event.objects.get(pk=event_id)
    category = Category.objects.get(pk=category_id, event=event)
    subcategory = SubCategory.objects.get(pk=subcategory_id, category=category)
    form = SubCategoryCreateForm(instance=subcategory)

    if request.POST:
        form = SubCategoryCreateForm(request.POST, instance=subcategory)
        if form.is_valid():
            form.save()
            return redirect('host:sub_categories', event_id=event_id, category_id=category_id)
        else:
            print(form.errors)

    context = {
        'form': form,
        'event': event,
        'category': category,
        'mode': 'Update'
    }

    return render(request, 'host/create_subcategory.html', context=context)


@allowed_users(['admin'])
def delete_subcategory(request, event_id, category_id, subcategory_id):
    event = Event.objects.get(pk=event_id)
    category = event.category_set.get(pk=category_id)
    category.subcategory_set.get(pk=subcategory_id).delete()
    return redirect('host:sub_categories', event_id=event_id, category_id=category_id)

