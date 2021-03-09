from typing import ContextManager
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.contrib import messages

from account.models import TeamLeaderModel
from .forms import PlayerCreateForm


# Create your views here.


def dashboard(request):
    pic_url = request.user.get_prof_pic_url()
    players = request.user.teamleadermodel.player_set.all()
    teams = request.user.teamleadermodel.team_set.all()
    context = {
        'pic_url': pic_url,
        'players': players,
        'teams': teams,
    }
    return render(request, 'team_leader/dashboard.html', context=context)


def player_list(request):
    player_list = request.user.teamleadermodel.player_set.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(player_list, 10)
    try:
        players = paginator.page(page)
    except:
        players = paginator.page(1)

    return render(request, 'team_leader/player_list.html', {'players': players})


def team_list(request):
    team_list = request.user.teamleadermodel.team_set.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(team_list, 10)
    try:
        teams = paginator.page(page)
    except:
        teams = paginator.page(1)

    return render(request, 'team_leader/team_list.html', {'teams': teams})


def add_player(request):
    form = PlayerCreateForm()

    if request.POST:
        form = PlayerCreateForm(request.POST, request.FILES)

        if form.is_valid():
            player = form.save(commit=False)
            player.teamleader = request.user.teamleadermodel
            player.save()
            messages.success(request, 'Successfully Registered.')
            return redirect('team_leader:players')
    context = {
        'form': form,
        'type': 'Player',
    }
    return render(request, 'team_leader/add_data.html', context=context)


def add_team(request):
    pass


def update_player(request):
    pass


def update_team(request):
    pass
