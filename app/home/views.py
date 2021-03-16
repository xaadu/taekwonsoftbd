from django.shortcuts import redirect, render

# Create your views here.

from host.models import Event, RegisteredTeam, RegisteredPlayer

from .forms import PlayerApplyForm, PlayerUpdateForm


def comingsoon(request):
    return render(request, 'comingsoon.html')


def events(request):
    objects = Event.objects.all()

    context = {
        'events': objects
    }

    return render(request, 'home/events.html', context)


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

    return render(request, 'home/event.html', context)


def event_teams(request, pk):
    event = Event.objects.get(pk=pk)
    teams = event.registeredteam_set.all()
    context = {
        'event': event,
        'teams': teams
    }

    return render(request, 'home/teams.html', context)


def event_team_details(request, event_id, reg_team_id):
    event = Event.objects.get(pk=event_id)
    team = event.registeredteam_set.get(pk=reg_team_id)
    players = team.registeredplayer_set.all()
    context = {
        'event': event,
        'team': team,
        'players': players
    }

    return render(request, 'home/team_details.html', context)


def event_players(request, pk):
    event = Event.objects.get(pk=pk)
    players = event.registeredplayer_set.all()
    context = {
        'event': event,
        'players': players
    }

    return render(request, 'home/players.html', context)


def manage(request, pk):
    event = Event.objects.get(pk=pk)
    teamData = {}
    try:
        teams = list(event.registeredteam_set.all())

        # Doesn't support in mysql
        # userTeams = request.user.teamleadermodel.registeredteam_set.filter(
        #    event_id=pk)
        #teams = teams.intersection(userTeams)

        userTeams = list(request.user.teamleadermodel.team_set.all())
        userTeamIDs = [user.id for user in userTeams]
        teams = [team for team in teams if team.team_id in userTeamIDs]

        for team in teams:
            teamData[team] = team.registeredplayer_set.all()

    except Exception as e:
        print(e)

    context = {
        'event': event,
        'teamData': teamData
    }

    return render(request, 'home/manage.html', context)


def event_team_update(request, event_id, reg_team_id):
    event = Event.objects.get(pk=event_id)
    team = event.registeredteam_set.get(pk=reg_team_id)
    players = request.user.teamleadermodel.player_set.all()
    player_ids = [player.id for player in players]
    # print(player_ids)
    categories = event.category_set.all()
    category_ids = [category.id for category in categories]
    # print(category_ids)

    if request.POST:
        # print(request.POST)
        post_data = dict(request.POST)
        data = dict()
        for key in post_data.keys():
            if key.startswith('player') and not key.startswith('player_'):
                data[int(key[6:])] = int(post_data['player_cat'+key[6:]][0])

        team.registeredplayer_set.all().delete()
        for player_id, category_id in data.items():
            #print(player_id, category_id)
            if player_id in player_ids and category_id in category_ids:
                x = RegisteredPlayer.objects.create(
                    event=event,
                    team=team,
                    player_id=player_id,
                    category_id=category_id
                )
                x.save()
                # print(x)

    context = {
        'players': players,
        'categories': categories,
    }

    return render(request, 'home/update.html', context)


def event_team_delete(request, event_id, reg_team_id):
    event = Event.objects.get(pk=event_id)
    event.registeredteam_set.get(pk=reg_team_id).delete()
    return redirect('home:manage', pk=event_id)


def apply(request, pk):
    event = Event.objects.get(pk=pk)
    teams = request.user.teamleadermodel.team_set.all()
    team_ids = [team.id for team in teams]
    players = request.user.teamleadermodel.player_set.all()
    player_ids = [player.id for player in players]
    categories = event.category_set.all()
    category_ids = [category.id for category in categories]

    if request.POST:
        # print(request.POST)
        post_data = dict(request.POST)
        data = dict()
        for key in post_data.keys():
            if key.startswith('player') and not key.startswith('player_'):
                data[int(key[6:])] = int(post_data['player_cat'+key[6:]][0])
        team_id = post_data.get('team', None)
        if team_id != None and int(team_id[0]) in team_ids:
            team_id = int(team_id[0])
            rt = RegisteredTeam(
                event=event,
                team_id=team_id
            )
            rt.save()
            team_id = rt.id
            for player_id, category_id in data.items():
                #print(player_id, category_id)
                if player_id in player_ids and category_id in category_ids:
                    x = RegisteredPlayer.objects.create(
                        event=event,
                        team_id=team_id,
                        player_id=player_id,
                        category_id=category_id
                    )
                    x.save()
                    # print(x)

    context = {
        'teams': teams,
        'players': players,
        'categories': categories,
    }

    return render(request, 'home/apply.html', context)
    event = Event.objects.get(pk=pk)
    form = PlayerApplyForm(request=request)

    if request.POST:
        form = PlayerApplyForm(request.POST, request=request)
        if form.is_valid():
            regTeam = form.save(commit=False)
            regTeam.event = event
            regTeam.save()
            regPlayers = form.cleaned_data.get('players')
            for player in regPlayers:
                rp = RegisteredPlayer.objects.create(
                    event=event,
                    team=regTeam,
                    player=player
                )
                # rp.player.set(player)
                rp.save()

    context = {
        'form': form
    }

    return render(request, 'home/apply.html', context)
