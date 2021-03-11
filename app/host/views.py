import os

from django.shortcuts import render, redirect
from django.contrib import messages

from account.decorators import allowed_users

from .forms import HostUpdateForm

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
