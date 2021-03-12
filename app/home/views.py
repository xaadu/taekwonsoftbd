from django.shortcuts import render

# Create your views here.

from host.models import Event, RegisteredPlayer

from .forms import PlayerApplyForm


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


def apply(request, pk):
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
