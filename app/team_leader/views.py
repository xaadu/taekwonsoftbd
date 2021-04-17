import os
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.contrib import messages

from account.models import TeamLeaderModel
from account.decorators import allowed_users
from .forms import PlayerCreateForm, TeamCreateForm, TLUpdateForm
from .models import Player, Team


# Create your views here.

@allowed_users(['tl'])
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


@allowed_users(['tl'])
def profile(request):
    pic_url = request.user.get_prof_pic_url()
    form = TLUpdateForm(instance=request.user, request=request)

    if request.POST:
        form = TLUpdateForm(request.POST, request.FILES,
                            instance=request.user, request=request)
        if form.is_valid():
            user = form.save()
            user.teamleadermodel.club_name = form.cleaned_data.get('club_name')
            user.teamleadermodel.save()
            messages.success(request, 'Profile Successfully Updated.')
            return redirect('team_leader:dashboard')

    context = {
        'pic_url': pic_url,
        'type': 'Team Leader',
        'form': form,
        'ipinfo_token': os.environ.get('IPLOOKUP_TOKEN'),
    }
    return render(request, 'prof_update.html', context)


@allowed_users(['tl'])
def player_list(request):
    pic_url = request.user.get_prof_pic_url()
    player_list = request.user.teamleadermodel.player_set.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(player_list, 10)
    try:
        players = paginator.page(page)
    except:
        players = paginator.page(1)

    context = {
        'pic_url': pic_url,
        'players': players,
    }

    return render(request, 'team_leader/player_list.html', context=context)


@allowed_users(['tl'])
def team_list(request):
    pic_url = request.user.get_prof_pic_url()
    team_list = request.user.teamleadermodel.team_set.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(team_list, 10)
    try:
        teams = paginator.page(page)
    except:
        teams = paginator.page(1)

    context = {
        'pic_url': pic_url,
        'teams': teams,
    }

    return render(request, 'team_leader/team_list.html', context=context)


@allowed_users(['tl'])
def add_player(request):
    pic_url = request.user.get_prof_pic_url()
    form = PlayerCreateForm()

    if request.POST:
        form = PlayerCreateForm(request.POST, request.FILES)

        if form.is_valid():
            player = form.save(commit=False)
            player.teamleader = request.user.teamleadermodel
            player.save()
            messages.success(request, 'Player Added Successfully.')
            return redirect('team_leader:players')
    context = {
        'form': form,
        'type': 'Member',
        'mode': 'Add',
        'pic_url': pic_url,
    }
    return render(request, 'team_leader/mod_data.html', context=context)


@allowed_users(['tl'])
def add_team(request):
    pic_url = request.user.get_prof_pic_url()
    form = TeamCreateForm()

    if request.POST:
        form = TeamCreateForm(request.POST)

        if form.is_valid():
            team = form.save(commit=False)
            team.teamleader = request.user.teamleadermodel
            team.save()
            messages.success(request, 'Team Added Successfully.')
            return redirect('team_leader:teams')
    context = {
        'form': form,
        'type': 'Team',
        'mode': 'Add',
        'pic_url': pic_url,
    }
    return render(request, 'team_leader/mod_data.html', context=context)


@allowed_users(['tl'])
def update_player(request, pk):
    pic_url = request.user.get_prof_pic_url()
    player = Player.objects.get(pk=pk)
    form = PlayerCreateForm(instance=player)

    if request.POST:
        form = PlayerCreateForm(request.POST, request.FILES, instance=player)

        if form.is_valid():
            player = form.save(commit=False)
            player.teamleader = request.user.teamleadermodel
            player.save()
            messages.success(request, 'Player Updated Successfully.')
            return redirect('team_leader:players')
    context = {
        'form': form,
        'type': 'Player',
        'mode': 'Update',
        'pic_url': pic_url,
    }
    return render(request, 'team_leader/mod_data.html', context=context)


@allowed_users(['tl'])
def update_team(request, pk):
    pic_url = request.user.get_prof_pic_url()
    team = Team.objects.get(pk=pk)
    form = TeamCreateForm(instance=team)

    if request.POST:
        form = TeamCreateForm(request.POST, instance=team)

        if form.is_valid():
            team = form.save(commit=False)
            team.teamleader = request.user.teamleadermodel
            team.save()
            messages.success(request, 'Team Updated Successfully.')
            return redirect('team_leader:teams')
    context = {
        'form': form,
        'type': 'Team',
        'mode': 'Update',
        'pic_url': pic_url,
    }
    return render(request, 'team_leader/mod_data.html', context=context)


@allowed_users(['tl'])
def remove_player(request, pk):
    Player.objects.get(pk=pk).delete()
    messages.success(request, 'Player Removed Successfully.')
    return redirect('team_leader:players')


@allowed_users(['tl'])
def remove_team(request, pk):
    Team.objects.get(pk=pk).delete()
    messages.success(request, 'Team Removed Successfully.')
    return redirect('team_leader:teams')
