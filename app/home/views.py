import os

from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages

# Create your views here.

from host.models import Event, RegisteredTeam, RegisteredPlayer, Category

from .forms import ContactForm, PlayerApplyForm, PlayerUpdateForm


def comingsoon(request):
    return render(request, 'comingsoon.html')


def home(request):
    return render(request, 'home/home.html')


def contact(request):
    form = ContactForm()

    if request.POST:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = f'Message from {form.cleaned_data["name"]}'
            sender = {form.cleaned_data["email"]}
            message = {form.cleaned_data["message"]}
            receipients = os.environ.get('CONTACT_RECIPIENTS').split(',')
            try:
                send_mail(subject, message, sender, receipients, fail_silently=True)
                messages.success(request, 'Email sent successfully!')
            except BadHeaderError:
                messages.error(request, 'Email Could not be send!')
            return redirect('home:home')

    context = {
        'form': form
    }
    return render(request, 'home/contact.html', context)


def about(request):
    return render(request, 'home/about.html')


def events(request):
    events = Event.objects.all()

    page = request.GET.get('page', 1)

    paginator = Paginator(events, 6)
    try:
        events = paginator.page(page)
    except:
        events = paginator.page(1)

    context = {
        'events': events
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


def result_categories(request, event_id):
    event = Event.objects.get(pk=event_id)
    categories = event.category_set.all()
    _categories = {}
    for category in categories:
        _categories[category] = len(category.registeredplayer_set.all())

    context = {
        'event': event,
        'categories': _categories,
    }

    return render(request, 'home/result_categories.html', context)


def results(request, event_id, category_id):
    event = Event.objects.get(pk=event_id)
    category = Category.objects.get(pk=category_id)
    players = category.registeredplayer_set.all()
    playerWithResults = dict()
    for player in players:
        roundResults = player.playerresult_set.all()
        finalPoint = 0
        for res in roundResults:
            finalPoint += res.accuracy+res.presentation
        try:
            finalPoint /= len(roundResults)
        except ZeroDivisionError:
            finalPoint = 0
        playerWithResults[player] = '{:.2f}'.format(finalPoint)

    context = {
        'event': event,
        'category': category,
        'playerWithResults': playerWithResults,
    }

    return render(request, 'home/results.html', context)
