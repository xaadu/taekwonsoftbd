from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.contrib import messages

from account.models import TeamLeaderModel
from .forms import PlayerCreateForm, TeamCreateForm
from .models import Player, Team


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
        'mode': 'Add',
    }
    return render(request, 'team_leader/mod_data.html', context=context)


def add_team(request):
    form = TeamCreateForm()

    if request.POST:
        form = TeamCreateForm(request.POST)

        if form.is_valid():
            team = form.save(commit=False)
            team.teamleader = request.user.teamleadermodel
            team.save()
            messages.success(request, 'Successfully Registered.')
            return redirect('team_leader:teams')
    context = {
        'form': form,
        'type': 'Team',
        'mode': 'Add',
    }
    return render(request, 'team_leader/mod_data.html', context=context)


def update_player(request, pk):
    player = Player.objects.get(pk=pk)
    form = PlayerCreateForm(instance=player)

    if request.POST:
        form = PlayerCreateForm(request.POST, request.FILES, instance=player)

        if form.is_valid():
            player = form.save(commit=False)
            player.teamleader = request.user.teamleadermodel
            player.save()
            messages.success(request, 'Successfully Registered.')
            return redirect('team_leader:players')
    context = {
        'form': form,
        'type': 'Player',
        'mode': 'Update',
    }
    return render(request, 'team_leader/mod_data.html', context=context)


def update_team(request, pk):
    team = Team.objects.get(pk=pk)
    form = TeamCreateForm(instance=team)

    if request.POST:
        form = TeamCreateForm(request.POST, instance=team)

        if form.is_valid():
            team = form.save(commit=False)
            team.teamleader = request.user.teamleadermodel
            team.save()
            messages.success(request, 'Successfully Registered.')
            return redirect('team_leader:teams')
    context = {
        'form': form,
        'type': 'Team',
        'mode': 'Update',
    }
    return render(request, 'team_leader/mod_data.html', context=context)


def remove_player(request, pk):
    Player.objects.get(pk=pk).delete()
    return redirect('team_leader:players')


def remove_team(request, pk):
    Team.objects.get(pk=pk).delete()
    return redirect('team_leader:teams')
